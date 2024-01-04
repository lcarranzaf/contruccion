from django.contrib import admin
from .models import UserModel,Planta,Guias,Tipo_Planta,LecturaHumedad
admin.site.register(LecturaHumedad)
admin.site.register(UserModel)
admin.site.register(Planta)
admin.site.register(Guias)
admin.site.register(Tipo_Planta)

# Register your models here.
