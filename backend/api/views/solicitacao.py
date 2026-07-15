from rest_framework import viewsets
from solicitacao.models import Solicitacao,ItemSolicitacao
from api.serializers.solicitacao import SolicitacaoSerializer, ItemSolicitacaoSerializer
from rest_framework.permissions import IsAuthenticated 
from api.permissions import AdminOuCria

class SolicitacaoViewSet(viewsets.ModelViewSet):
    queryset = Solicitacao.objects.all()
    serializer_class = SolicitacaoSerializer
    permission_classes = [AdminOuCria]
    

class ItemSolicitacaoViewSet(viewsets.ModelViewSet):
    queryset = ItemSolicitacao.objects.all()
    serializer_class = ItemSolicitacaoSerializer
    permission_classes = [AdminOuCria]
    