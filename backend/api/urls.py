from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.catalogo import CategoriaViewSet, ProdutoViewSet
from api.views.dashboard import DashboardAPIView, ExportarRelatorioCSVView
from api.views.loja import LojaViewSet
from api.views.solicitacao import ItemSolicitacaoViewSet, SolicitacaoViewSet
from api.views.usuario import UsuarioView

router = DefaultRouter()

# Rota da Loja
router.register(r'loja', LojaViewSet, basename='loja')

# Rotas do Catálogo (suporta singular e plural para evitar incompatibilidade com o Vue)
router.register(r'produtos', ProdutoViewSet, basename='produtos')
router.register(r'produto', ProdutoViewSet, basename='produto')

router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'categoria', CategoriaViewSet, basename='categoria')

# Rotas de Solicitações
router.register(r'solicitacoes', SolicitacaoViewSet, basename='solicitacoes')
router.register(r'solicitacao', SolicitacaoViewSet, basename='solicitacao')
router.register(r'item-solicitacao', ItemSolicitacaoViewSet, basename='item-solicitacao')


urlpatterns = [
    # Inclui os endpoints do router
    path('', include(router.urls)),

    # Endpoints de Usuário e Dashboard
    path('me/', UsuarioView.as_view(), name='me'),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
    path('dashboard/exportar-csv/', ExportarRelatorioCSVView.as_view(), name='dashboard-exportar-csv'),
]