# Importaciones necesarias para las vistas
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from .models import Evento, RegistroEvento
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, EventoForm

from django.utils import timezone
from django.db.models import Count

# Vista principal
def inicio(request):
    return render(request, 'inicio.html')

# Vista de registro utilizando el modelo User por defecto de Django
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, "Usuario registrado con éxito.")
                return redirect('inicio')
            except IntegrityError:
                form.add_error('email', 'Este correo ya está registrado.')
        else:
            print(form.errors)  # Para depuración

    else:
        form = RegistroForm()

    return render(request, 'registro_form.html', {'form': form})

# Vista de inicio de sesión
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Buscar al usuario usando el correo electrónico
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user and check_password(password, user.password):
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso")
            return redirect('listarEventos')
        else:
            messages.error(request, "Correo o contraseña inválidos")
            return render(request, 'inicio.html')

    return render(request, 'inicio.html')

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('inicio')

# Vista para listar eventos
def listarEventos(request):
    eventos = Evento.objects.all()
    registros_usuario = RegistroEvento.objects.filter(usuario=request.user) if request.user.is_authenticated else []

    eventos_registrados = {registro.evento.id for registro in registros_usuario}

    context = {
        'eventos': eventos,
        'eventos_registrados': eventos_registrados
    }

    return render(request, 'eventos/listarEventos.html', context)

# Vista para mostrar detalles de un evento
def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'eventos/detalleEvento.html', {'evento': evento})

# Vista para crear un nuevo evento
@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user  # Asigna el usuario autenticado como organizador
            evento.save()
            return redirect('listarEventos')  # Redirige después de crear el evento
    else:
        form = EventoForm()
    return render(request, 'eventos/crear_evento.html', {'form': form})

# Vista para editar un evento
@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user  # Asegurarse de que el organizador sea el usuario autenticado
            evento.save()
            return redirect('listarEventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/editar_evento.html', {'form': form, 'evento': evento})

# Vista para eliminar un evento
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        evento.delete()
        return redirect('listarEventos')  # Redirige a la lista de eventos después de eliminar
    return render(request, 'eventos/eliminar_evento.html', {'evento': evento})

# Vista para registrarse en un evento
@login_required
def registrarse_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    usuario = request.user

    # Verificar si el usuario ya está registrado en el evento
    registro_existente = RegistroEvento.objects.filter(usuario=usuario, evento=evento).exists()

    if registro_existente:
        messages.error(request, 'Ya estás registrado en este evento.')
    else:
        # Crear el registro del usuario para el evento
        RegistroEvento.objects.create(usuario=usuario, evento=evento)
        messages.success(request, 'Te has registrado exitosamente en el evento.')

    return redirect('listarEventos', evento_id=evento.id)

# Vista para ver los usuarios registrados en un evento
def ver_registrados(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    registrados = RegistroEvento.objects.filter(evento=evento)

    context = {
        'evento': evento,
        'registrados': registrados,
    }
    return render(request, 'eventos/ver_registrados.html', context)

# Vista para el panel de estadísticas de eventos
def panel_vistas(request):
    # Asegúrate de que el usuario esté autenticado antes de acceder a su ID
    if request.user.is_authenticated:
        # Pregunta 1: ¿Cuántos eventos se están llevando a cabo este mes?
        hoy = timezone.now()
        inicio_mes = hoy.replace(day=1)
        fin_mes = (inicio_mes + timezone.timedelta(days=32)).replace(day=1)
        eventos_mes_actual = Evento.objects.filter(fechaInicio__gte=inicio_mes, fechaInicio__lt=fin_mes).count()

        # Pregunta 2: ¿Quiénes son los usuarios más activos en términos de participación en eventos?
        usuarios_activos = RegistroEvento.objects.values('usuario__username').annotate(num_eventos=Count('evento')).order_by('-num_eventos')

        # Pregunta 3: ¿Cuántos eventos ha organizado el usuario autenticado?
        eventos_organizados = Evento.objects.filter(organizador=request.user).count()  # Contamos los eventos organizados por el usuario

        context = {
            'eventos_mes_actual': eventos_mes_actual,
            'usuarios_activos': usuarios_activos,
            'eventos_organizados': eventos_organizados,  # Aquí se envía la cantidad de eventos organizados por el usuario
        }

        return render(request, 'eventos/panel_vistas.html', context)  # Renderiza el panel de estadísticas
    else:
        # Redirigir a una página de inicio de sesión o mostrar un mensaje si el usuario no está autenticado
        return redirect('inicio')
