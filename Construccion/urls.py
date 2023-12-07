from django.contrib import admin
from django.urls import path
from Proyects.views import signup, login,index,plantas,about,sensor,escaner,mostrar_plantas,ver_guia,misplantas,reconocimiento_plantas
from django.conf import settings
from django.conf.urls.static import static


urlpatterns =[
    path('admin/', admin.site.urls),
    path('',login,name='home'),
    path('',signup, name='signup'),
    path('login/', login, name='login'),
    path('index/', index, name='index'),
    path('plantas/',plantas, name='plantas'),
    path('misplantas/',misplantas, name='misplantas'),
    path('about/',about, name='about'),
    path('sensor/',sensor, name='sensor'),
    path('escaner/',escaner, name='escaner'),
    path('mostrar-plantas/', mostrar_plantas, name='mostrar_plantas'),
    path('ver_guia/<int:planta_id>/', ver_guia, name='ver_guia'),
    path('reconocimiento/', reconocimiento_plantas, name='reconocimiento_plantas'),
    ]

    


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

