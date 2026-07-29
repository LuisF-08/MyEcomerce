from rest_framework.routers import DefaultRouter
from django.urls import path, include

from api.views.catalogo import CategoriaViewSet, ProdutoViewSet
from api.views.loja import LojaViewSet
from api.views.solicitacao import SolicitacaoViewSet, ItemSolicitacaoViewSet
from api.views.usuario import UsuarioView
from api.views.dashboard import DashboardAPIView, ExportarRelatorioCSVView


router = DefaultRouter()

router.register(r'loja', LojaViewSet, basename='loja')
router.register(r'produto', ProdutoViewSet, basename='produto')
router.register(r'categoria', CategoriaViewSet, basename='categoria')
router.register(r'solicitacao', SolicitacaoViewSet, basename='solicitacao')
router.register(
    r'item-solicitacao',
    ItemSolicitacaoViewSet,
    basename='item-solicitacao'
)


urlpatterns = [
    path('api/', include(router.urls)),

    path(
        'api/me',
        UsuarioView.as_view(),
        name='me'
    ),

    path(
        'api/dashboard/',
        DashboardAPIView.as_view(),
        name='dashboard'
    ),

    path(
        'api/dashboard/exportar-csv/',
        ExportarRelatorioCSVView.as_view(),
        name='dashboard-exportar-csv'
    ),
]