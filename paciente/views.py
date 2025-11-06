from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Pacientes, Profile
from .models import Insumo

from django.shortcuts import render, redirect
from .models import Pacientes, cita

# Create your views here.
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'error':''
        })
    else:
       print (request.POST)
       user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
       print (user)
       if user is None:
           return render (request, 'login.html', {
               'error':'Usuario o contraseña incorrecta'
           })
       else:
           login(request, user)
           return render (request, 'base.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def base(request):
    return render(request, 'base.html')

@login_required
def agendarCi(request):
    return render(request, 'agendarCi.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Pacientes, cita
from django.contrib import messages

def agendarCi(request):
    citas = cita.objects.select_related('paciente').all()
    return render(request, 'agendarCi.html', {'citas': citas})


def agendarCi_guardar(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        motivo = request.POST.get('motivo')

        paciente, creado = Pacientes.objects.get_or_create(
            cedula=cedula,
            defaults={
                'nombre': nombre,
                'apellido': apellido,
                'direccion': '',
                'celular': '',
                'fecha_nacimiento': '2000-01-01',
                'estado_civil': 'soltero',
                'edad': 0,
                'correo': '',
                'tipo_sangre': '',
                'fecha_cita': fecha,
                'hora_cita': hora,
                'tipo_tratamiento': motivo,
            }
        )

        cita.objects.create(
            paciente=paciente,
            fecha_cita=fecha,
            hora_cita=hora,
            tipo_tratamiento=motivo
        )

        messages.success(request, "✅ Cita agendada correctamente.")
        return redirect('agendarCi')

    return redirect('agendarCi')


def editar_cita(request, id):
    c = get_object_or_404(cita, id=id)

    if request.method == 'POST':
        c.fecha_cita = request.POST['fecha_cita']
        c.hora_cita = request.POST['hora_cita']
        c.tipo_tratamiento = request.POST['tipo_tratamiento']
        c.save()
        return redirect('agendarCi')

    return render(request, 'editar_cita.html', {'c': c})


def eliminar_cita(request, id):
    c = get_object_or_404(cita, id=id)
    c.delete()
    messages.success(request, "🗑️ Cita eliminada correctamente.")
    return redirect('agendarCi')


@login_required
def ubicacion(request):
    return render(request, 'ubicacion.html')

@login_required
def documentacion(request):
    return render(request, 'documentacion.html')

@login_required
def registroInsu(request):
    # Mostrar la tabla con insumos
    insumos = Insumo.objects.all()
    return render(request, 'registroInsu.html', {'insumos': insumos})

def crear_insumo(request):
    if request.method == 'POST':
        print("ENTRÓ A LA VISTA CREAR")

        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        observacion = request.POST.get('observacion')

        Insumo.objects.create(
            nombre=nombre,
            cantidad=cantidad,
            fecha_ingreso=fecha_ingreso,
            observacion=observacion
        )
        messages.success(request, 'Insumo registrado correctamente.')
        return redirect('registroInsu')
    else:
        # Si entras con GET, solo redirige o muestra formulario (opcional)
        return redirect('registroInsu')
def editar_insumo(request, pk):
    insumo = get_object_or_404(insumos, pk=pk)
    if request.method == 'POST':
        insumo.nombre = request.POST.get('nombre')
        insumo.cantidad = request.POST.get('cantidad')
        insumo.fecha_ingreso = request.POST.get('fecha_ingreso')
        insumo.observacion = request.POST.get('observacion')
        insumo.save()
        messages.success(request, 'Insumo actualizado correctamente.')
        return redirect('registroInsu')
    return render(request, 'editar_insumo.html', {'insumo': insumo})
def eliminar_insumo(request, pk):
    insumo = get_object_or_404(insumos, pk=pk)
    if request.method == 'POST':
        insumo.delete()
        messages.success(request, 'Insumo eliminado correctamente.')
        return redirect('registroInsu')
    return render(request, 'eliminar_insumo.html', {'insumo': insumo})
