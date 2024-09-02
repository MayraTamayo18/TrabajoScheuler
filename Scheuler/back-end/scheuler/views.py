
import threading

from django.conf import settings
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.utils import timezone

from .models import UsuarioModifica
from django.shortcuts import get_object_or_404, render
from scheduler import Scheduler
from scheduler.trigger import Sunday

from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .serializer import  UserSerializer





@api_view(['POST'])
def iniciarSesion(request):
    
    user = get_object_or_404(UsuarioModifica, email=request.data['email'])
    
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
        if UsuarioModifica.objects.filter(email=request.data.get('email')).exists():
            return Response({'error': 'El usuario ya se encuentra registrado'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            #crea el token y lo guarda
            token = Token.objects.create(user=user)
            #funcion para enviar correo
            def send_email():
                subject = 'Bienvenid@'
                from_email = settings.EMAIL_HOST_USER
                to = request.data.get('email')
                text_content = 'Gracias por registrarte en TuVooz.'
                html_content = render_to_string('correoRegistro.html', {'subject': subject, 'message': text_content})

                email = EmailMultiAlternatives(subject, text_content, from_email, [to])
                email.attach_alternative(html_content, "text/html")
                email.send() 
                
                # Iniciar el envío del correo en un hilo separado
                email_thread = threading.Thread(target=send_email)
                email_thread.start()
            
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#acceso al perfil
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def perfil(request):
    
    return Response("Usted está iniciando sesión con {}".format(request.user.email), status=status.HTTP_200_OK)

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<EJEMPLOD PROFESOR<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#def TaskNotificacion():
#    print('ejecutando tarea')
    
#simula la tarea del envio de notificaciones     
#scheduler = Scheduler()
#scheduler.cyclic(dt.timedelta(seconds=1), TaskNotificacion)    

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Configuramos el Scheduler
# crea-programador-ejecuta las tareas en segundo plano  con intervalo de tiempo
scheduler = BackgroundScheduler()

#<<<<<<<<<<<<<<<<<<<<<<<<< 18 años <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# función vercificacion 18-años
def verificar_usuarios():
    #optenemos la hora y fecha actual 
    hoy = datetime.now() 
    # Trae-datos-model de Usuario
    usuarios = UsuarioModifica.objects.all() 

    # for-recorrer cada usuarios registrados
    for usuario in usuarios:

        # verifica si el Docuemneto es "TI" entonces
        if usuario.tipoDocumento == 'TI':
            #Obtiene la fecha de nacimiento del usuario
            fecha_nacimiento = usuario.fechaNacimiento
        #Se procede a hacer la resta del año actual con el año de nacimiento 
            if fecha_nacimiento:
                # aqui se calcula la edad:añoNacimiento - añoActual  ajustando por la fecha de nacimiento.
                                                           # meses de diferencias y los dias 
                edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
               #usuario tiene 18 años o más, se llama a la función mostrarNotificacion
                if edad >= 18:
                    mostrarNotificacion(usuario)
def mostrarNotificacion(usuario):
    # Imprimir el mensaje en la terminal
    print(f"<<<<Alerta: Actualización de datos, el usuario {usuario.username} con número de documento {usuario.numeroDocumento} se debe actualizar sus datos.")
    
#<<<<<<<<<<<<<<<<<<<<<<<<< contraseña <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#función contraseña
def notificarCambioContrasena():
    #optenemos la hora y fecha actual 
    hoy = datetime.now() 
    # Trae datos del Usuario 
    usuarios = UsuarioModifica.objects.all() 
    
    # recorrer cada usuarios y imprime un mensaje si deben cambiar su contraseña
    for usuario in usuarios:
    
        print(f"<<<<Alerta: Cambio de contraseña, el usuario {usuario.username} debe cambiar su contraseña por seguridad.")

#<<<<<<<<<<<<<<<<<<<<<<<<< inactividad <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# función inactividad 

def verificarInactividad():
    hoy = timezone.now() 
    # Calcula la fecha que fue exactamente hace un mes desde hoy.
    un_mes_atras = hoy - timedelta(days=30)
    # Trae datos Usuario 
    usuarios = UsuarioModifica.objects.all() 

    # recorre usuarios 
    for usuario in usuarios:
        # Si el ultimo inicio de sesión está en None o es Null db
        if usuario.last_login is None:
            # Omite el usuario
            continue  

        # Verifica si el último inicio de sesión del usuario fue hace más de un mes.
        if usuario.last_login < un_mes_atras:
            
            #desactiva la cuenta del usuario.
            usuario.is_active = False 
            # Guarda los cambios.
            usuario.save() 
            #un mensaje de alerta .
            print(f"<<<<Alerta: su cuenta se bloqueo {usuario.username} ya que no se conecta desde {usuario.last_login}. Se procederá a bloquear la cuenta por seguridad.")
            
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<            
# 15 segundos va a decir que usuario esta con TI teniendo 18
scheduler.add_job(verificar_usuarios, IntervalTrigger(seconds=10)) 
scheduler.add_job(notificarCambioContrasena, IntervalTrigger(seconds=15)) 
scheduler.add_job(verificarInactividad, IntervalTrigger(seconds=10)) 

# Ponemos a correr el scheduler
scheduler.start() 

