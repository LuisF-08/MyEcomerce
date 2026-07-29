from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_spectacular.utils import extend_schema

from api.permissions import AdminOuLeitura
from api.serializers.catalogo import CategoriaSerializer, ProdutoSerializer
from catalogo.models import Categoria, Produto


@extend_schema(
    request=ProdutoSerializer,
    responses=ProdutoSerializer,
)
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [AdminOuLeitura]

    # DICA: Adicionar JSONParser permite aceitar JSON no Swagger/Postman além de Form-Data
    parser_classes = (
        MultiPartParser,
        FormParser,
        JSONParser,
    )

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    # Campos utilizados para filtragem exata ou por faixa (ex: ?preco__gte=100)
    filterset_fields = {
        "categoria": ["exact"],
        "ativo": ["exact"],
        "destaque": ["exact"],
        "preco": ["exact", "gte", "lte"],
        "quantidade": ["exact", "gte", "lte"],
    }

    # Campos de Busca (?search=termo)
    # No DRF, por padrão já usa icontains
    search_fields = (
        "nome",
        "descricao",
    )

    # Campos de ordenação (?ordering=preco ou ?ordering=-preco)
    ordering_fields = (
        "nome",
        "preco",
        "quantidade",
        "criado_em",
    )
    
    # Ordenação Principal padrão
    ordering = ("-criado_em",)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AdminOuLeitura]