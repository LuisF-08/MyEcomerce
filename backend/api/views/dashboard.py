from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import DashboardService


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Nomes de variáveis melhorados para refletir estatísticas/cards 
        cards = DashboardService.obter_cards_gerais()
        pedidos_mes = DashboardService.obter_pedidos_por_mes()
        produtos_mais_vendidos = DashboardService.obter_produtos_mais_vendidos()
        ultimos_pedidos = DashboardService.obter_ultimos_pedidos()

        return Response({
            "cards": cards,
            "grafico_pedidos": pedidos_mes,
            "produtos_mais_vendidos": produtos_mais_vendidos,
            "ultimos_pedidos": ultimos_pedidos
        })


class ExportarRelatorioCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="relatorio_solicitacoes.csv"'
        
        # O service popula diretamente o response para 
        # evitar carregar tudo em memória à toa
        return DashboardService.gerar_relatorio_csv(response)