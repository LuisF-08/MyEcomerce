# api/serializers/usuario.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UsuarioSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='first_name', required=True)
    
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password] 
    )

    class Meta:
        model = User
        fields = ['id', 'nome', 'email', 'password']

    def create(self, validated_data):
        
        email = validated_data['email']
        
        user = User.objects.create_user(
            username=email, 
            email=email,
            first_name=validated_data.get('first_name', ''),
            password=validated_data['password']
        )
        return user