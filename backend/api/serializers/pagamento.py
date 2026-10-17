from rest_framework import serializers
from solicitacao.models import Solicitacao

class CriarPagamentoSerializer(serializers.Serializer):
    solicitacao = serializers.PrimaryKeyRelatedField(
        queryset=Solicitacao.objects.all()
    )
    
class ConfirmarPagamentoSerializer(serializers.Serializer):
    payment_id = serializers.RegexField(r"^\d{1,20}$")