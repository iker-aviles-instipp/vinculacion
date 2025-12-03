from django.contrib.auth.models import Group, User
from autenticacion.models import Profile
from paciente.models import Pacientes, cita, Insumo, Documento 
from .serializers import (
    UserSerializer, GroupSerializer, ProfileSerializer, 
    PacientesSerializer, CitaSerializer, InsumoSerializer, DocumentoSerializer 
)
from rest_framework import viewsets
from rest_framework import permissions

# Vistas de autenticación (si ya las tienes, usa las que tienes)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

# VISTAS DE DATOS CLÍNICOS (NUEVAS)
class PacientesViewSet(viewsets.ModelViewSet):
    queryset = Pacientes.objects.all()
    serializer_class = PacientesSerializer
    # Permiso: Solo los usuarios autenticados pueden acceder
    permission_classes = [permissions.IsAuthenticated]

class CitaViewSet(viewsets.ModelViewSet):
    queryset = cita.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [permissions.IsAuthenticated]

class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    permission_classes = [permissions.IsAuthenticated]

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]