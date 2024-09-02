from django.db import models
from django.contrib.auth.models import AbstractUser
#sobre escribimos la tabla y la hacemos mia y agregamos lo que nos hace falta 
class UsuarioModifica(AbstractUser):
    tipoDocumento = models.CharField(max_length=3, blank=True, null=True)
    numeroDocumento = models.CharField(max_length=13, blank=True, null=True)
    fechaNacimiento = models.DateField(blank=True, null=True)

    
    
    
    
    