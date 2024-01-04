from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User
from .models import Planta,Guias, UsuarioPlanta, Tipo_Planta, LecturaHumedad
from django.shortcuts import render, get_object_or_404
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
from googletrans import Translator
import serial.tools.list_ports
import serial   
import time
#vista de registro
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')

        # Verifica que la contraseña tenga al menos 5 caracteres
        if len(password1) < 5:
            messages.error(request, 'La contraseña debe tener al menos 5 caracteres.')
            return redirect('signup')

        try:
            # Verifica si el nombre de usuario ya existe
            existing_user = User.objects.get(username=username)
            messages.error(request, 'El nombre de usuario ya existe. Por favor, elige otro.')
            return redirect('signup')
        except User.DoesNotExist:
            # El usuario no existe, procede con la creación
            user = User.objects.create_user(
                username=username,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            auth_login(request, user)
            return redirect('login')
    else:
        return render(request, 'login/login.html')

#vista de inicio
def index(request):
    return render(request, 'index/index.html')

#vista de inicio de sesion
def login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth_login(request, user)
            return redirect('index')  
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

# vista de cerrar sesion
def cerrar_sesion(request):
    logout(request)
    return redirect('login')

#vista de las guias
def ver_guia(request, planta_id):
    planta = get_object_or_404(Planta, pk=planta_id)
    guia = planta.guia
    if guia:
        return render(request, 'guia/guia.html', {'planta': planta, 'guia': guia})
    else:
        return render(request, 'sin_guia.html', {'planta': planta})

#vista de reconocimiento de plantas
    
def reconocimiento_plantas(request):
    if request.method == 'POST' and request.FILES.get('imagen'):
        cliente_vision = vision_v1.ImageAnnotatorClient.from_service_account_file('C:/Users/anaXD/Downloads/prueba1.0/prueba1.0/PROYECTO/plantfriend-407202-6b1b21ee4a87.json')

        imagen = request.FILES['imagen'].read()

        imagen = types.Image(content=imagen)

        image_context = types.ImageContext(language_hints=["es"])

        respuesta = cliente_vision.label_detection(image=imagen, image_context=image_context)
        etiquetas = respuesta.label_annotations

        lista = [etiqueta.description for etiqueta in etiquetas]
        if 'Plant' in lista:
            if 'Food' in lista or 'Natural Foods' in lista:
                mejor_etiqueta = [lista[0], lista[3], lista[4], lista[6]]
                
            else:
                mejor_etiqueta = None
                mensaje_no_planta = 'La imagen no contiene una planta reconocida.'
                
                # Traduce el mensaje al español
                translator = Translator()
                mensaje_no_planta_es = translator.translate(mensaje_no_planta, dest='es').text

                return render(request, 'resultado/resultado_reconocimiento.html', {'mensaje_no_planta': mensaje_no_planta_es})
        else:
            mejor_etiqueta = None
            mensaje_no_planta = 'La imagen no contiene una planta reconocida.'

            translator = Translator()
            mensaje_no_planta_es = translator.translate(mensaje_no_planta, dest='es').text

            return render(request, 'resultado/resultado_reconocimiento.html', {'mensaje_no_planta': mensaje_no_planta_es})   
  
        translator = Translator()
        mejor_etiqueta_es = [translator.translate(etiqueta, dest='es').text for etiqueta in mejor_etiqueta]
        
        imagen_url = request.FILES['imagen'].url if hasattr(request.FILES['imagen'], 'url') else ''

        return render(request, 'resultado/resultado_reconocimiento.html', {'nombre_planta': mejor_etiqueta_es, 'imagen_url': imagen_url})


    return render(request, 'escaner/escaner.html')

#vista para agregar planta a usuario

@login_required
def agregar_planta_a_usuario(request, planta_id):
    planta = get_object_or_404(Planta, idplanta=planta_id)
    
    if UsuarioPlanta.objects.filter(usuario=request.user, planta=planta).exists():
        
        return redirect('mostrar_plantas')  

    if request.method == 'POST':
        usuario = request.user
        usuario_planta = UsuarioPlanta(usuario=usuario, planta=planta)
        usuario_planta.save()
        return redirect('misplantas')  

    return render(request, 'misplantas/misplantas.html', {'planta': planta})

#vista de mis plantas
@login_required
def misplantas(request):
    usuario_plantas = UsuarioPlanta.objects.filter(usuario=request.user)
    return render(request, 'misplantas/misplantas.html', {'usuario_plantas': usuario_plantas})

#elimina plantas
@login_required
def eliminar_planta(request, usuario_planta_id):
    usuario_planta = get_object_or_404(UsuarioPlanta, id=usuario_planta_id, usuario=request.user)

    if request.method == 'POST':
        usuario_planta.delete()
        return redirect('misplantas')
    return render(request, 'misplantas/eliminaplanta.html', {'usuario_planta': usuario_planta})

@login_required
def eliminar_planta_confirmar(request, usuario_planta_id):
    usuario_planta = get_object_or_404(UsuarioPlanta, id=usuario_planta_id, usuario=request.user)
    
    if request.method == 'POST':
        usuario_planta.delete()
        return redirect('misplantas')
    
    return render(request, 'misplantas/eliminaplanta.html', {'usuario_planta': usuario_planta})

#vista de inicio de sesion 
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            messages.error(request, 'La contraseña ingresada es incorrecta.')

    return render(request, 'login/inicio.html')

def mostrar_plantas(request):
    plantas = Planta.objects.all()

    tipos = Tipo_Planta.objects.all()
    tipos_serialized = serialize('json', tipos)

    tipo_seleccionado = request.GET.get('tipo', None)
    tipo_seleccionado_nombre = None

    if tipo_seleccionado:
        plantas = plantas.filter(tipo__idtipo=tipo_seleccionado)
        tipo_seleccionado_nombre = Tipo_Planta.objects.get(idtipo=tipo_seleccionado).nombre

    context = {
        'plantas': plantas,
        'tipos_serialized': tipos_serialized,  
        'tipo_seleccionado': tipo_seleccionado,
        'tipo_seleccionado_nombre': tipo_seleccionado_nombre,
        'tipos':tipos
    }
    return render(request, 'mostrar_plantas/mostrar_plantas.html', context)


# Configura el puerto serie
ser = serial.Serial('COM3', 9600)

# def leer_humedad():
#     try:
#         time.sleep(2)  # Espera para asegurarse de que Arduino esté listo
#         ser.flush()     # Limpia el buffer del puerto serial
#         ser.write(b'L')  # Envía una señal para que Arduino calcule y envíe la humedad
#         if ser.in_waiting > 0:
#             linea = ser.readline().decode('utf-8').rstrip()
#             partes = linea.split(": ")
#             if partes[0] == 'Humedad':
#                 valor_humedad = partes[1]
#                 if valor_humedad == 'N/A':
#                     return None
#                 return valor_humedad
#     except Exception as e:
#         print(e)
#     finally:
#         ser.close()
def leer_humedad():
    try:
        with serial.Serial('COM3', 9600) as ser:
            time.sleep(2)
            ser.flush()
            ser.write(b'L')
            if ser.in_waiting > 0:
                linea = ser.readline().decode('utf-8').rstrip()
                partes = linea.split(": ")
                if partes[0] == 'Humedad':
                    valor_humedad = partes[1]
                    if valor_humedad == 'N/A':
                        return None
                    return valor_humedad
    except Exception as e:
        print(e)
        return None


# def vista_humedad(request):
#     humedad = leer_humedad()
#     print(humedad)
#     if isinstance(humedad, str):
#         humedad = int(humedad.replace('%', ''))
#     else: 
#         humedad = 0
#     return render(request, 'humedad/humedad.html', {
#         'humedad': humedad,
#     })
def vista_humedad(request):
    try:
        humedad = leer_humedad()
        print(humedad)
        if isinstance(humedad, str):
            humedad = int(humedad.replace('%', ''))
        else: 
            humedad = 0
    except Exception as e:
        print(e)
        humedad = 0  # O manejar de acuerdo a tus necesidades

    return render(request, 'humedad/humedad.html', {
        'humedad': humedad,
    })