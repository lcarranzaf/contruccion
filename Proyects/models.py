from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.utils import timezone

class Guias(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion= models.CharField(max_length=2000)
    imagen = models.ImageField(upload_to='plant_images/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    

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
    
class Planta(models.Model):
   nombre = models.CharField(max_length=100)
   comentario = models.TextField()
   imagen = models.ImageField(upload_to='plant_images/', blank=True, null=True)
   guia = models.ForeignKey(Guias, on_delete=models.CASCADE, null=True)
   usuarios = models.ManyToManyField(UserModel, through='UsuarioPlanta')

   def __str__(self):
       return self.nombre

class UsuarioPlanta(models.Model):
    usuario = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.name} - {self.planta.nombre}'







class PlantaRegistro(models.Model):
    nombre_planta = models.CharField(max_length=200)
    fecha_riego = models.DateField()
    comentario = models.TextField()
    ruta_imagen = models.ImageField(upload_to='imagenes/')
    valor_humedad = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
       return self.nombre_planta
    
    
    def __str__(self):
        return self.nombre
    

    