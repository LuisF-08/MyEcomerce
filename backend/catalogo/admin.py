from django.contrib import admin
from catalogo.models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "categoria",
        "preco",
        "quantidade",
        "ativo",
        "destaque",
    )

    list_filter = (
        "categoria",
        "ativo",
        "destaque",
    )

    search_fields = (
        "nome",
        "descricao",
    )

    list_editable = (
        "preco",
        "quantidade",
        "ativo",
    )