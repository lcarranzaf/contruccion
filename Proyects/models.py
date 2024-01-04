from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.contrib.auth.models import User as UserModel

#tabla de guias
class Guias(models.Model):
    nombre = models.CharField(max_length=250)
    comentario= models.TextField()
    imagen = models.ImageField(upload_to='plant_guide/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    
#tabla de registro
class UserModel(models.Model):
    userId=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,blank=False)
    lastname=models.CharField(max_length=255,blank=False)
    email = models.EmailField(max_length=254, help_text='Required. Enter a valid email address.', unique=True,blank=False)
    password=models.CharField(max_length=250,blank=False)
    creationDate=models.DateTimeField(auto_now_add=True)
    updateDate=models.DateTimeField(auto_now=True)
    def __str__(self) :
        return self.name
#tabla de tipos de plantas
class Tipo_Planta(models.Model):
    idtipo=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

#tabla de Pantas
class Planta(models.Model):
   idplanta = models.AutoField(primary_key=True)
   nombre = models.CharField(max_length=100)
   comentario = models.TextField()
   imagen = models.ImageField(upload_to='plant_images/', blank=True, null=True)
   guia = models.ForeignKey(Guias, on_delete=models.CASCADE, null=True)
   usuarios = models.ManyToManyField(User, through='UsuarioPlanta')
   tipo = models.ForeignKey(Tipo_Planta, on_delete=models.SET_NULL, null=True)
   def __str__(self):
       return self.nombre

#tabla de usuarios que tienen plantas
class UsuarioPlanta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.planta.nombre}'

class LecturaHumedad(models.Model):
    valor_humedad = models.CharField(max_length=4)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    # usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # planta = models.ForeignKey(Planta, on_delete=models.CASCADE)



    def _str_(self):
        return f"Humedad: {self.valor_humedad}% - {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}"