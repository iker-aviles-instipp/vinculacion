from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   telefono = models.CharField(max_length=15, blank=True, null=True)
   fecha_nacimiento = models.DateField(blank=True, null=True)
   direccion = models.CharField(max_length=255, blank=True, null=True)
   cedula = models.CharField(max_length=15, blank=True, null=True)

   def __str__(self):
        return f"{self.user.username}'s profile"
    
class Pacientes(models.Model):
    nombre = models.CharField(max_length=225)
    apellido = models.CharField(max_length=225)
    cedula = models.CharField(max_length=15)
    direccion = models.CharField(max_length=225)
    celular = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField(verbose_name='fecha_nacimiento')
    estado_civil = models.CharField(max_length=28, verbose_name='estado civil')
    edad = models.IntegerField()
    correo = models.EmailField(max_length=225, null=True)
    tipo_sangre = models.CharField(max_length=3, null=True, verbose_name='tipo de sangre')
    fecha_cita = models.DateField(max_length=225)
    hora_cita = models.TimeField(max_length=1000)
    tipo_tratamiento =models.EmailField(null=True)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class cita(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()
    tipo_tratamiento = models.CharField(max_length=100)

    def __str__(self):
        return f"Cita de {self.paciente.nombre} {self.paciente.apellido} para el {self.fecha_cita} a las {self.hora_cita}"

class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    fecha_ingreso = models.DateField()
    observacion = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.nombre
     
class Documento(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    nombre_documento = models.CharField(max_length=255, default='Documento de Observación') 
    fecha_creacion = models.DateField(auto_now_add=True)
    # 🚨 NUEVO CAMPO: Campo de texto para las observaciones
    observaciones = models.TextField(blank=True, null=True) 
    
    def __str__(self):
        return f'Documento de {self.paciente.nombre} {self.paciente.apellido} - {self.nombre_documento}'
    
class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    fecha_ingreso = models.DateField()
    ultima_actualizacion = models.DateField(auto_now=True) # Este es el campo que falta en la DB
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre