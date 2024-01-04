from django.contrib import admin
from django.urls import path
from Proyects.views import signup, login,index,plantas,about,sensor,mostrar_plantas,ver_guia,misplantas,reconocimiento_plantas,cerrar_sesion,agregar_planta_a_usuario,eliminar_planta,eliminar_planta_confirmar,vista_humedad
from django.conf import settings
from django.conf.urls.static import static


urlpatterns =[
    path('admin/', admin.site.urls),
    path('',login,name='home'),
    path('signup/',signup, name='signup'),
    path('login/', login, name='login'),
    path('index/', index, name='index'),
    path('plantas/',plantas, name='plantas'),
    path('misplantas/',misplantas, name='misplantas'),
    path('about/',about, name='about'),
    path('sensor/',sensor, name='sensor'),
    path('mostrar-plantas/', mostrar_plantas, name='mostrar_plantas'),
    path('ver_guia/<int:planta_id>/', ver_guia, name='ver_guia'),
    path('reconocimiento/', reconocimiento_plantas, name='reconocimiento_plantas'),
    path('cerrar-sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('agregar_planta_a_usuario/<int:planta_id>/', agregar_planta_a_usuario, name='agregar_planta_a_usuario'),
    path('eliminar_planta/<int:usuario_planta_id>/', eliminar_planta, name='eliminar_planta'),
    path('eliminar_planta/<int:usuario_planta_id>/confirmar/', eliminar_planta_confirmar, name='eliminar_planta_confirmar'),
    path('humedad/', vista_humedad, name='vista_humedad'),
    ]

    


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

