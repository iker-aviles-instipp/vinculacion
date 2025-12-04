from django.contrib.auth.models import User, Group
from rest_framework import serializers
# El modelo Profile está definido en paciente/models.py, así que la importación es correcta.
from paciente.models import Profile, Pacientes, cita, Insumo, Documento 

# =================================================================
# 1. SERIALIZADORES DE AUTENTICACIÓN Y PERFIL
# =================================================================

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """Serializador para el modelo Profile (el Perfil extendido del Usuario)."""
    class Meta:
        model = Profile
        # Campos de tu modelo Profile según paciente/models.py (cedula, telefono, direccion)
        fields = ['url', 'cedula', 'telefono', 'direccion', 'user']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializador para el modelo User de Django."""
    # Añadimos el perfil anidado para ver los datos extendidos del usuario
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email', 'groups', 'date_joined', 'profile']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """Serializador para los grupos de usuarios de Django."""
    class Meta:
        model = Group
        fields = ['url', 'name']

# =================================================================
# 2. SERIALIZADORES DE DATOS CLÍNICOS
# =================================================================

class DocumentoSerializer(serializers.HyperlinkedModelSerializer):
    """Serializador para el modelo Documento."""
    class Meta:
        model = Documento
        fields = ['url', 'paciente', 'nombre_documento', 'observaciones', 'fecha_creacion']

class CitaSerializer(serializers.HyperlinkedModelSerializer):
    """Serializador para el modelo cita."""
    class Meta:
        model = cita
        fields = ['url', 'paciente', 'fecha_cita', 'hora_cita', 'tipo_tratamiento']

class InsumoSerializer(serializers.HyperlinkedModelSerializer):
    """Serializador para el modelo Insumo."""
    class Meta:
        model = Insumo
        fields = ['url', 'nombre', 'cantidad', 'fecha_ingreso', 'observacion']

class PacientesSerializer(serializers.HyperlinkedModelSerializer):
    """Serializador para el modelo Pacientes, incluyendo citas y documentos anidados."""
    # Muestra la lista de citas (many=True) que tiene este paciente.
    citas = CitaSerializer(many=True, read_only=True, source='cita_set')
    # Muestra la lista de documentos (many=True) que tiene este paciente.
    documentos = DocumentoSerializer(many=True, read_only=True, source='documento_set')
    
    class Meta:
        model = Pacientes
        fields = [
            'url', 'nombre', 'apellido', 'cedula', 'celular', 'fecha_nacimiento', 
            'edad', 'correo', 'tipo_sangre', 'citas', 'documentos'
        ]