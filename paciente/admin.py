from django.contrib import admin
from .models import Pacientes, Insumo, cita, Profile

# Register your models here.
admin.site.register(Pacientes)
admin.site.register(Insumo) 