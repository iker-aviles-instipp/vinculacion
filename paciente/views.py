from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Pacientes, Profile
from .models import Insumo

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

def agendarCi_guardar(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        direccion = request.POST.get('direccion')
        celular = request.POST.get('celular')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        estado_civil = request.POST.get('estado_civil')
        edad = request.POST.get('edad')
        correo = request.POST.get('correo')
        tipo_sangre = request.POST.get('tipo_sangre')
        fecha_cita = request.POST.get('fecha_cita')
        hora_cita = request.POST.get('hora_cita')
        tipo_tratamiento = request.POST.get('tipo_tratamiento')

        cita = Pacientes(
            nombres=nombres,
            apellido=apellido,
            cedula=cedula,
            direccion=direccion,
            celular=celular,
            fecha_nacimiento=fecha_nacimiento,
            estado_civil=estado_civil,
            edad=edad,
            correo=request.POST.get('correo'),
            tipo_sangre=tipo_sangre,
            fecha_cita=fecha_cita,
            hora_cita=hora_cita,
            tipo_tratamiento=tipo_tratamiento
        )
        cita.save()
        messages.success(request, 'Cita agendada correctamente.')
        return redirect('base')

    return render(request, 'agendarCi.html')

def agendarCi_editar(request, pk):
    cita = get_object_or_404(Pacientes, pk=pk)
    if request.method == 'POST':
        cita.nombre = request.POST.get('nombres')
        cita.apellido = request.POST.get('apellido')
        cita.cedula = request.POST.get('cedula')
        cita.direccion = request.POST.get('direccion')
        cita.celular = request.POST.get('celular')
        cita.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        cita.estado_civil = request.POST.get('estado_civil')
        cita.edad = request.POST.get('edad')
        cita.correo = request.POST.get('correo')
        cita.tipo_sangre = request.POST.get('tipo_sangre')
        cita.fecha_cita = request.POST.get('fecha_cita')
        cita.hora_cita = request.POST.get('hora_cita')
        cita.tipo_tratamiento = request.POST.get('tipo_tratamiento')
        cita.save()
        messages.success(request, 'Cita actualizada correctamente.')
        return redirect('base')
    return render(request, 'agendarCi_editar.html', {'cita': cita})


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
