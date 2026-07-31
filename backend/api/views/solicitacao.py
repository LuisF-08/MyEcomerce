from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from solicitacao.models import Solicitacao, ItemSolicitacao
from api.serializers.solicitacao import (
    SolicitacaoSerializer,
    ItemSolicitacaoSerializer,
)
from api.permissions import AdminOuCria


class SolicitacaoViewSet(viewsets.ModelViewSet):

    queryset = Solicitacao.objects.prefetch_related(
        "itens"
    ).all()

    serializer_class = SolicitacaoSerializer

    permission_classes = [AdminOuCria]

    @action(
        detail=True,
        methods=["patch"],
        url_path="status"
    )
    def alterar_status(self, request, pk=None):

        solicitacao = self.get_object()

        novo_status = request.data.get("status")

        if not novo_status:
            return Response(
                {
                    "status": "O status é obrigatório."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        solicitacao.status = novo_status
        solicitacao.save(update_fields=["status"])

        serializer = self.get_serializer(solicitacao)

        return Response(serializer.data)


class ItemSolicitacaoViewSet(viewsets.ModelViewSet):

    queryset = ItemSolicitacao.objects.all()

    serializer_class = ItemSolicitacaoSerializer

    permission_classes = [AdminOuCria]
