from rest_framework import serializers
from loja.models import Loja
import re

class LojaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loja
        fields = "__all__"
        
    def validate_nome(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "O nome da loja é obrigatório."
            )

        return value
    
    def validate_whatsapp(self, value):
        numero = re.sub(r"\D", "", value)
        if len(numero) < 10:
            raise serializers.ValidationError(
                "Informe um WhatsApp válido."
            )

        return value
    
    def validate_cor_primaria(self,  value):
        if not HEX_COLOR.match(value):
            raise serializers.ValidationError(
            "Informe uma cor hexadecimal válida. Ex: #4100A2"
            )

        return value.upper()
    
    def validate_cor_secundaria(self,  value):
        if not HEX_COLOR.match(value):
            raise serializers.ValidationError(
            "Informe uma cor hexadecimal válida. Ex: #4100A2"
            )

        return value.upper()
    