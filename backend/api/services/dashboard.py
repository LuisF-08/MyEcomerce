import csv
from django.db.models import Sum, Avg, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from decimal import Decimal
from solicitacao.models import Solicitacao, ItemSolicitacao, StatusSolicitacao
from catalogo.models import Produto

# Constantes de legibilidade 
LIMITE_ULTIMOS_PEDIDOS = 5
LIMITE_PRODUTOS_MAIS_VENDIDOS = 5

class DashboardService:

    @staticmethod
    def obter_cards_gerais():
        """
        Retorna as estatísticas rápidas do dashboard (cards).
        Nomes descritivos (Ponto 8) e tratamento de Decimal (Ponto 7).
        """
        solicitacoes_concluidas = Solicitacao.objects.filter(
            status=StatusSolicitacao.CONCLUIDO  
        )

        # Faturamento total das solicitações concluídas
        faturamento = solicitacoes_concluidas.aggregate(
            total=Sum("total")
        )["total"] or Decimal("0.00")

        # Média de produtos por pedido calculada dinamicamente 
        ticket_medio = solicitacoes_concluidas.aggregate(
                media=Avg("total")
            )["media"] or Decimal("0.00")

        # Total de novos pedidos
        novos_pedidos = Solicitacao.objects.filter(
            status=StatusSolicitacao.NOVO  
        ).count()

        # Total geral de solicitações
        total_pedidos = Solicitacao.objects.count()

        return {
            "faturamento": round(float(faturamento), 2),
            "pedidos_novos": novos_pedidos,
            "total_pedidos": total_pedidos,
            "produto_medio": round(float(ticket_medio), 2)
        }

    @staticmethod
    def obter_pedidos_por_mes():
        """
        Retorna a evolução de pedidos e faturamento agrupados por mês.
        """
        pedidos_mes = (
            Solicitacao.objects.filter(status=StatusSolicitacao.CONCLUIDO)
            .annotate(mes=TruncMonth("criado_em"))
            .values("mes")
            .annotate(
                quantidade=Count("id"),
                total_faturamento=Sum("total")
            )
            .order_by("mes")
        )

        dados_grafico = []
        for p in pedidos_mes:
            faturamento_mes = p["total_faturamento"] or Decimal("0.00")
            dados_grafico.append({
                "mes": p["mes"].strftime("%B/%Y") if p["mes"] else "N/A",
                "quantidade": p["quantidade"],
                "total": round(float(faturamento_mes), 2)
            })

        return dados_grafico

    @staticmethod
    def obter_produtos_mais_vendidos():
        """
        Retorna a lista de produtos mais vendidos usando o relacionamento correto (Ponto 2).
        Utiliza 'itens_solicitados' que é o related_name definido no seu ItemSolicitacao.
        """
        produtos = (
            Produto.objects.annotate(
                quantidade_vendida=Sum("itens_solicitados__quantidade")
            )
            .filter(quantidade_vendida__gt=0)
            .order_by("-quantidade_vendida")[:LIMITE_PRODUTOS_MAIS_VENDIDOS]
        )

        return [
            {
                "id": prod.id,
                "nome": prod.nome,
                "quantidade_vendida": prod.quantidade_vendida
            }
            for prod in produtos
        ]

    @staticmethod
    def obter_ultimos_pedidos():
        """
        Retorna os últimos pedidos formatados, já incluindo telefone,
        localização e itens do pedido para exibição no card do dashboard.
        """
        ultimos = Solicitacao.objects.all().order_by("-criado_em")[:LIMITE_ULTIMOS_PEDIDOS]
    
        resultado = []
    
        for u in ultimos:
            itens = [
                {
                    "produto_nome": item.produto_nome,
                    "quantidade": item.quantidade,
                }
                for item in ItemSolicitacao.objects.filter(solicitacao=u)
            ]
    
            resultado.append({
                "id": u.id,
                "cliente": u.nome,
                "telefone": u.telefone,
                "cidade": u.cidade,
                "estado": u.estado,
                "total": round(float(u.total), 2),
                "status": u.get_status_display(),
                "criado_em": u.criado_em.isoformat(),
                "itens": itens,
            })
    
        return resultado
        
    @staticmethod
    def gerar_relatorio_csv(response):
        """
        Escreve o relatório de solicitações diretamente no response HTTP.
        Adiciona mais colunas úteis e formata de forma limpa (Ponto 5).
        """
        writer = csv.writer(response)
        
        # Cabeçalho robusto 
        writer.writerow([
            "ID",
            "Cliente",
            "Telefone",
            "Cidade",
            "Total",
            "Status",
            "Criado em"
        ])

        solicitacoes = Solicitacao.objects.all().order_by("-criado_em")

        for s in solicitacoes:
            data_formatada = timezone.localtime(s.criado_em).strftime("%d/%m/%Y %H:%M")
            writer.writerow([
                s.id,
                s.nome,
                s.telefone,
                s.cidade,
                round(float(s.total), 2),
                s.get_status_display(),
                data_formatada
            ])
        
        return response