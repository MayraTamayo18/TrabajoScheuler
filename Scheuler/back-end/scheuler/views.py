
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render


from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializer import  UserSerializer, UsuarioSerializer
from .models import Usuario




@api_view(['POST'])
def iniciarSesion(request):
    
    user = get_object_or_404(User, email=request.data['email'])
    
    if not user.check_password(request.data['password']):
        return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
     #aqui retorna el token
    return Response({"token": token.key}, status=status.HTTP_200_OK)

#registro de usuario
@api_view(['POST'])
def registro(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        print(request.data)
        # Verificar si el usuario ya existe por email
        if User.objects.filter(email=request.data.get('email')).exists():
            return Response({'error': 'El usuario ya se encuentra registrado'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            #crea el token y lo guarda
            token = Token.objects.create(user=user)
            
            # def send_email():
            #     subject = 'Bienvenid@ a tu Vooz'
            #     from_email = settings.EMAIL_HOST_USER
            #     to = request.data.get('email')
            #     text_content = 'Gracias por registrarte en TuVooz.'
            #     html_content = render_to_string('correoRegistro.html', {'subject': subject, 'message': text_content})

            #     email = EmailMultiAlternatives(subject, text_content, from_email, [to])
            #     email.attach_alternative(html_content, "text/html")
            #     email.send()
            
            # send_email()
            
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#acceso al perfil
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def perfil(request):
    
    return Response("Usted está iniciando sesión con {}".format(request.user.email), status=status.HTTP_200_OK)


class UsuarioView(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()
