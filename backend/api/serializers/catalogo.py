from rest_framework import serializers
from catalogo.models import Categoria, Produto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
        
    def validate_nome(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "O nome da loja é obrigatório."
            )

        return value
    
    def validate_ordem(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Ordem deve ser maior ou igual a 0"
            )
        return value


class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(
        source="categoria.nome",
        read_only=True
    )

    class Meta:
        model = Produto
        fields = [
            "id",
            "nome",
            "descricao",
            "preco",
            "imagem_1",
            "imagem_2",
            "categoria",
            "categoria_nome",
            "destaque",
            "ativo",
            "quantidade"
        ]

    def validate_nome(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
            "O nome deve possuir pelo menos 3 caracteres."
            )
        return value

    def validate_preco(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "O preço deve ser maior que zero."
            )

        return value

    def validate(self, attrs):

        if attrs["quantidade"] == 0 and attrs["ativo"]:
            raise serializers.ValidationError(
                "Produto sem estoque não pode ficar ativo."
            )
    
        if attrs.get("destaque") and not attrs.get("ativo"):
            raise serializers.ValidationError(
                "Um produto em destaque deve estar ativo."
            )
    
        return attrs