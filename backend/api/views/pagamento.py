from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.pagamento import CriarPagamentoSerializer
from api.services.pagamento import ErroMercadoPago, criar_preferencia
from pagamento.models import Pagamento
from solicitacao.models import StatusSolicitacao


class CriarPagamentoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CriarPagamentoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        solicitacao = serializer.validated_data["solicitacao"]

        # Só gera link para pedidos que realmente aguardam pagamento
        if solicitacao.status != StatusSolicitacao.AGUARDANDO_PAGAMENTO:
            return Response(
                {"detail": "Esta solicitação não está aguardando pagamento."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Itens e preços saem do BD, nunca da requisição/front
        itens = [
            {
                "id": item.produto_id or item.pk,
                "titulo": item.produto_nome,
                "quantidade": item.quantidade,
                "preco": item.preco_unitario,
            }
            for item in solicitacao.itens.all()
        ]

        try:
            resultado = criar_preferencia(
                itens=itens,
                external_reference=solicitacao.pk,
            )
        except ErroMercadoPago:
            return Response(
                {"detail": "Não foi possível iniciar o pagamento. Tente novamente."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        pagamento = Pagamento.objects.create(
            solicitacao=solicitacao,
            preference_id=resultado["preference_id"],
            valor=solicitacao.total,
        )

        return Response(
            {
                "pagamento_id": pagamento.pk,
                "init_point": resultado["init_point"],
            },
            status=status.HTTP_201_CREATED,
        )