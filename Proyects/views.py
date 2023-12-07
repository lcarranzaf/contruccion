from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User
from .models import Planta,Guias
from django.shortcuts import render, get_object_or_404
from google.cloud import vision_v1
from google.cloud.vision_v1 import types


def prueba(request):
    return HttpResponse("holiii")

def signup(request):
    if request.method == 'POST':
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'], 
                email=request.POST['email']
            )
            user.save()
            print(user)
            auth_login(request, user)
            return redirect('login')
    else:
        return render(request, 'login/login.html')


def index(request):
    return render(request, 'index/index.html')

def login(request):
    if request.method == 'POST':
        # Autenticar al usuario
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth_login(request, user)
            return redirect('index')  # Cambiar 'index' por la URL deseada después del login
        else:
            messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')
    return render(request, 'login/login.html')

def misplantas(request):
    return render(request, 'misplantas/misplantas.html')

def plantas(request):
    return render(request, 'plantas/plantas.html')

def about(request):
    return render(request, 'about/about.html')

def sensor(request):
    return render(request, 'sensor/sensor.html')

def escaner(request):
    return render(request, 'escaner/escaner.html')

# --------------------------------------------


def mostrar_plantas(request):
    plantas = Planta.objects.all()
    return render(request, 'mostrar_plantas/mostrar_plantas.html', {'plantas': plantas})



def ver_guia(request, planta_id):
    planta = get_object_or_404(Planta, pk=planta_id)
    
    # Accede a la guía asociada a la planta
    guia = planta.guia

    if guia:
        # Si hay una guía asociada, muestra la información
        return render(request, 'guia/guia.html', {'planta': planta, 'guia': guia})
    else:
        # Si no hay guía asociada, puedes manejarlo según tus necesidades
        return render(request, 'sin_guia.html', {'planta': planta})

#vista del escaneo
def reconocimiento_plantas(request):
    if request.method == 'POST' and request.FILES.get('imagen'):
        # Configura la conexión a la API de Google Cloud Vision
        cliente_vision = vision_v1.ImageAnnotatorClient.from_service_account_file('C:/Users/anaXD/Downloads/PROYECTO1/PROYECTO/plantfriend-407202-6b1b21ee4a87.json')

        # Obtiene la imagen del request
        imagen = request.FILES['imagen'].read()

        # Convierte la imagen a formato compatible con Cloud Vision API
        imagen = types.Image(content=imagen)

        # Configura el contexto de la imagen para el idioma español
        image_context = types.ImageContext(language_hints=["es"])

        # Realiza la detección de etiquetas usando Cloud Vision API
        respuesta = cliente_vision.label_detection(image=imagen, image_context=image_context)
        etiquetas = respuesta.label_annotations

        # Itera sobre las etiquetas para encontrar la más relevante
        mejor_etiqueta = None
        mejor_score = 0.0

        for etiqueta in etiquetas:
            if etiqueta.score > mejor_score:
                mejor_etiqueta = etiqueta.description
                mejor_score = etiqueta.score

        return render(request, 'resultado/resultado_reconocimiento.html', {'nombre_planta': mejor_etiqueta, 'score_planta': mejor_score})

    return render(request, 'escaner/escaner.html')