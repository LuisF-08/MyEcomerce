from rest_framework import viewsets
from loja.models import Loja
from api.serializers.loja import LojaSerializer
from rest_framework.permissions import AllowAny
from api.permissions import AdminOuLeitura

class LojaViewSet(viewsets.ModelViewSet):
    queryset = Loja.objects.all()
    serializer_class = LojaSerializer
    permission_classes = [AdminOuLeitura]