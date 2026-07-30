from rest_framework import serializers
from django.utils.text import slugify
from catalogo.models import Categoria, Produto

class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = "__all__"
        read_only_fields = ["slug"]


    def gerar_slug_unico(
        self,
        nome,
        instance=None
    ):

        slug_base = slugify(nome)

        if not slug_base:
            raise serializers.ValidationError({
                "nome": "Não foi possível gerar um slug válido para este nome."
            })

        slug = slug_base
        contador = 1

        queryset = Categoria.objects.all()

        if instance:
            queryset = queryset.exclude(
                id=instance.id
            )

        while queryset.filter(
            slug=slug
        ).exists():

            slug = f"{slug_base}-{contador}"
            contador += 1

        return slug


    def create(self, validated_data):

        validated_data["slug"] = self.gerar_slug_unico(
            validated_data["nome"]
        )

        return Categoria.objects.create(
            **validated_data
        )


    def update(
        self,
        instance,
        validated_data
    ):

        if "nome" in validated_data:

            validated_data["slug"] = (
                self.gerar_slug_unico(
                    validated_data["nome"],
                    instance
                )
            )

        return super().update(
            instance,
            validated_data
        )


    def validate_nome(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O nome da categoria é obrigatório."
            )

        return value


    def validate_ordem(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "A ordem deve ser maior ou igual a 0."
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