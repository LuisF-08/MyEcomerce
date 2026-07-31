from decimal import Decimal
from django.db import transaction
from rest_framework import serializers

from solicitacao.models import Solicitacao, ItemSolicitacao
from catalogo.models import Produto


class ItemSolicitacaoSerializer(serializers.ModelSerializer):
    produto = serializers.PrimaryKeyRelatedField(
        queryset=Produto.objects.all()
    )

    class Meta:
        model = ItemSolicitacao
        fields = [
            "id",
            "solicitacao",
            "produto",
            "produto_nome",
            "preco_unitario",
            "quantidade",
            "subtotal",
            "variacao",
            "criado_em",
        ]

        read_only_fields = [
            "id",
            "solicitacao",
            "produto_nome",
            "preco_unitario",
            "subtotal",
            "criado_em",
        ]

        extra_kwargs = {
            "variacao": {
                "required": False,
                "allow_blank": True,
            }
        }

    def validate_quantidade(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "A quantidade do item deve ser maior que zero."
            )

        return value


class SolicitacaoSerializer(serializers.ModelSerializer):

    itens = ItemSolicitacaoSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Solicitacao

        fields = [
            "id",
            "nome",
            "telefone",
            "email",
            "cep",
            "rua",
            "numero",
            "referencia",
            "bairro",
            "cidade",
            "estado",
            "observacao",
            "total",
            "mensagem",
            "status",
            "itens",
            "criado_em",
        ]

        read_only_fields = [
            "id",
            "total",
            "mensagem",
            "criado_em",
            "itens",
        ]

    @transaction.atomic
    def create(self, validated_data):

        total_solicitacao = Decimal("0.00")

        solicitacao = Solicitacao.objects.create(
            total=Decimal("0.00"),
            **validated_data
        )

        # Aqui não será usado pelo painel administrativo.
        # Se a criação de solicitações pelo frontend continuar
        # sendo feita por esta API, os itens precisam ser tratados
        # separadamente ou recebidos em um serializer específico.

        solicitacao.total = total_solicitacao

        solicitacao.mensagem = (
            f"Olá {solicitacao.nome}! "
            f"Recebemos sua solicitação no valor de "
            f"R$ {total_solicitacao:.2f}. "
            "Entraremos em contato pelo WhatsApp."
        )

        solicitacao.save()

        return solicitacao
