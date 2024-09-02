from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UsuarioModifica
#importar la tabla mia

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioModifica
        #aqui llamo lo que le voy a pedir el usuario al ingresar
        fields = ['id', 'username', 'email', 'password', 'tipoDocumento', 'numeroDocumento','fechaNacimiento']
    def create(self, validated_data):
        user = UsuarioModifica.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            tipoDocumento=validated_data.get('tipoDocumento',''),
            numeroDocumento=validated_data.get('numeroDocumento',''),
            fechaNacimiento=validated_data.get('fechaNacimiento', None)
            
        )
        return user
    #se trae los campos que añadio
    
# class UsuarioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Usuario
#         fields = '__all__'