from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from api.permissions import AdminOuLeitura
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser

from api.serializers.catalogo import (
    CategoriaSerializer,
    ProdutoSerializer,
)
from catalogo.models import Categoria, Produto

@extend_schema(
    request=ProdutoSerializer,
    responses=ProdutoSerializer,
)
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [AdminOuLeitura]

    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    # Campos utlizados para filtragem 
    filterset_fields = {
        "categoria": ["exact"],
        "ativo": ["exact"],
        "destaque": ["exact"],
        "preco": ["exact", "gte", "lte"],
        "quantidade": ["exact", "gte", "lte"],
    }

    # campos de Busca
    search_fields = (
        "nome",
        "descricao",
    )

    # campos de ordenação
    ordering_fields = (
        "nome",
        "preco",
        "quantidade",
        "criado_em",
    )
    
    #Ordenação Pprincipal
    ordering = ("-criado_em",)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AdminOuLeitura]