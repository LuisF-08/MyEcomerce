from django.contrib import admin
from .models import Loja


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "cidade",
        "telefone",
        "ativo",
    )

    list_filter = (
        "ativo",
        "cidade",
    )

    search_fields = (
        "nome",
        "cidade",
        "email",
    )

    prepopulated_fields = {
        "slug": ("nome",)
    }