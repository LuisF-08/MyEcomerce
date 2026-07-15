from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from solicitacao.models import Solicitacao, ItemSolicitacao
from catalogo.models import Produto


class ItemSolicitacaoSerializer(serializers.ModelSerializer):
    produto = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all())
    
    class Meta:
        model = ItemSolicitacao
        fields = ["produto", "quantidade", "variacao"]
        extra_kwargs = {
            "variacao": {"required": False, "allow_blank": True}
        }

    #  Validar quantidade maior que zero 
    def validate_quantidade(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "A quantidade do item deve ser maior que zero."
            )
        return value


class SolicitacaoSerializer(serializers.ModelSerializer):
    itens = ItemSolicitacaoSerializer(many=True)

    class Meta:
        model = Solicitacao
        fields = [
            "id", "nome", "telefone", "email", "cep", "rua", "numero", 
            "referencia", "bairro", "cidade", "estado", "observacao", 
            "total", "mensagem", "status", "itens", "criado_em"
        ]
        # total e mensagem agora são calculados pelo backend
        read_only_fields = ["total", "mensagem"]

    # --- PONTO 4: Tornar a criação ATÔMICA (Tudo ou Nada) ---
    @transaction.atomic
    def create(self, validated_data):
        itens_data = validated_data.pop("itens")
        
        # Inicializar total usando Decimal ---
        total_solicitacao = Decimal("0.00")
        
        # Criamos a Solicitação principal com total temporário de 0
        solicitacao = Solicitacao.objects.create(total=Decimal("0.00"), **validated_data)
        
        # Processar cada item enviado no JSON
        for item_data in itens_data:
            produto = item_data["produto"]
            quantidade = item_data["quantidade"]
            variacao = item_data.get("variacao", "")
            
            #  Verificar se o produto está ativo/disponível
            if not getattr(produto, "ativo", True):
                raise serializers.ValidationError(
                    f"O produto '{produto.nome}' está indisponível para compras no momento."
                )
            
            #  Verificar estoque
            estoque_atual = getattr(produto, "quantidade", 0)
            if quantidade > estoque_atual:
                raise serializers.ValidationError(
                    f"Não há estoque suficiente para '{produto.nome}'. Estoque disponível: {estoque_atual}."
                )
            
            # Atualizar subtotal automaticamente usando valores seguros do banco 
            preco_unitario = Decimal(str(produto.preco))  # Garante tipo Decimal para operações matemáticas precisas
            subtotal = preco_unitario * quantidade
            total_solicitacao += subtotal
            
            # Criação do item de forma instanciada
            item = ItemSolicitacao(
                solicitacao=solicitacao,
                produto=produto,
                produto_nome=produto.nome,
                preco_unitario=preco_unitario,
                quantidade=quantidade,
                subtotal=subtotal,
                variacao=variacao
            )
            
            item.save()
            
            #  Descontar estoque e desativar se zerar ---
            produto.quantidade -= quantidade
            if produto.quantidade == 0:
                produto.ativo = False  # Desativa o produto se o estoque esgotou
            produto.save()

        # Mensagem de retorno personalizada e amigável 
        solicitacao.total = total_solicitacao
        solicitacao.mensagem = (
            f"Olá {solicitacao.nome}! "
            f"Recebemos sua solicitação no valor de "
            f"R$ {total_solicitacao:.2f}. "
            "Entraremos em contato pelo WhatsApp."
        )
        
        solicitacao.save()
        return solicitacao