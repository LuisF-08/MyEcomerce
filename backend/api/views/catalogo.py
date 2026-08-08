from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.core.cache import cache
from api.permissions import AdminOuLeitura
from api.serializers.catalogo import CategoriaSerializer, ProdutoSerializer
from catalogo.models import Categoria, Produto


# PRODUTOS
@extend_schema(
    request=ProdutoSerializer,
    responses=ProdutoSerializer,
)
class ProdutoViewSet(viewsets.ModelViewSet):

    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [AdminOuLeitura]

    # Permite JSON, FormData e upload de imagens
    parser_classes = (
        MultiPartParser,
        FormParser,
        JSONParser,
    )

    # Filtros
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = {
        "categoria": ["exact"],
        "ativo": ["exact"],
        "destaque": ["exact"],
        "preco": ["exact", "gte", "lte"],
        "quantidade": ["exact", "gte", "lte"],
    }

    # Busca
    search_fields = (
        "nome",
        "descricao",
    )

    # Ordenação
    ordering_fields = (
        "nome",
        "preco",
        "quantidade",
        "criado_em",
    )

    ordering = ("-criado_em",)


    # LISTAR PRODUTOS
    def list(self, request, *args, **kwargs):

        # Cria uma chave diferente para cada combinação

        query_string = request.META.get("QUERY_STRING", "")

        cache_key = f"produtos:{query_string}"

        # Tenta buscar no Redis
        produtos = cache.get(cache_key)

        if produtos is not None:

            print(f"[REDIS] Cache encontrado: {cache_key}")

            return Response(produtos)

        print(f"[REDIS] Cache não encontrado: {cache_key}")

        response = super().list(request, *args, **kwargs)
        cache.set(
            cache_key,
            response.data,
            timeout=300,
        )

        print(f"[REDIS] Cache salvo: {cache_key}")

        return response


    # CRIAR PRODUTO
    def perform_create(self, serializer):

        serializer.save()
        # todos os caches de produtos podem estar desatualizados.
        self._limpar_cache_produtos()

    # ATUALIZAR PRODUTO
    def perform_update(self, serializer):

        serializer.save()

        # O produto foi alterado.
        self._limpar_cache_produtos()

    # EXCLUIR PRODUTO
    def perform_destroy(self, instance):

        instance.delete()
        # Os caches precisam ser recriados.
        self._limpar_cache_produtos()


    # LIMPAR CACHE DE PRODUTOS
    def _limpar_cache_produtos(self):
        """
        Remove todas as chaves relacionadas aos produtos.
        """

        try:

            cache.delete_pattern("produtos:*")
            print("[REDIS] Cache de produtos limpo.")

        except AttributeError:

            # Fallback caso o backend de cache não suporte
            cache.clear()
            print("[REDIS] Cache limpo completamente.")


# Catalogo
class CategoriaViewSet(viewsets.ModelViewSet):

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AdminOuLeitura]

    parser_classes = (
        MultiPartParser,
        FormParser,
        JSONParser,
    )

