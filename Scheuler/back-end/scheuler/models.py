from django.db import models

# Create your models here.

class Usuario(models.Model):
    TI = 'TI'
    CC = 'CC'
    CE = 'CE'
    
    Tipo_Documento= [
        (TI, 'TI'),
        (CC, 'CC'), 
        (CE, 'CE'),  
    ]
    tipoDocumento= models.CharField(choices=Tipo_Documento, max_length=100)
    
    numeroDocumento= models.IntegerField(max_length=10)
    fechaNacimiento= models.DateField()
    clave=models.CharField(max_length=13)
    fechaActualizacionClave=models.DateField()
    fechaInicioSesion=models.DateField()
    correo=models.CharField(max_length=150)
    notificado=models.BooleanField(default=False)
    
    activo = 'Activo'
    inactivo = 'Inactivo'
    
    Tipo_estado_inicioSesion= [
        (activo, 'Activo'),
        (inactivo, 'inactivo'),   
    ]
    estado_inicioSesion= models.CharField(choices=Tipo_estado_inicioSesion, max_length=20)
    
    def __str__(self):
        return self.tipoDocumento


    
    
    
    