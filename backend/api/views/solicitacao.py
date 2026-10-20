from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from solicitacao.models import Solicitacao, ItemSolicitacao
from api.serializers.solicitacao import (
    SolicitacaoSerializer,
    ItemSolicitacaoSerializer,
)
from api.permissions import AdminOuCria
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework.permissions import AllowAny
from api.serializers.solicitacao import CheckoutSerializer

class SolicitacaoViewSet(viewsets.ModelViewSet):

    queryset = Solicitacao.objects.prefetch_related(
        "itens"
    ).all()

    serializer_class = SolicitacaoSerializer

    permission_classes = [IsAdminUser]

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
        
        if novo_status not in StatusSolicitacao.values:
            return Response({
                "status": "Status inválido."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        solicitacao.status = novo_status
        solicitacao.save(update_fields=["status"])
        
        authentication_classes = []

        serializer = self.get_serializer(solicitacao)

        return Response(serializer.data)


class ItemSolicitacaoViewSet(viewsets.ModelViewSet):

    queryset = ItemSolicitacao.objects.all()

    serializer_class = ItemSolicitacaoSerializer
    
    permission_classes = [IsAdminUser]
    
class CheckoutView(generics.CreateAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
