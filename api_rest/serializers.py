from django.contrib.auth.models import User, Group
from rest_framework import serializers

class DocumentoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Documento
        fields = ['url', 'paciente', 'nombre_documento', 'observaciones', 'fecha_creacion']

class CitaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = cita
        fields = ['url', 'paciente', 'fecha_cita', 'hora_cita', 'tipo_tratamiento']

class InsumoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Insumo
        fields = ['url', 'nombre', 'cantidad', 'fecha_ingreso', 'observacion']

class PacientesSerializer(serializers.HyperlinkedModelSerializer):
    # Opcional: Para mostrar las citas y documentos asociados directamente en el paciente.
    citas = CitaSerializer(many=True, read_only=True, source='cita_set')
    documentos = DocumentoSerializer(many=True, read_only=True, source='documento_set')
    
    class Meta:
        model = Pacientes
        fields = [
            'url', 'nombre', 'apellido', 'cedula', 'celular', 'fecha_nacimiento', 
            'edad', 'correo', 'tipo_sangre', 'citas', 'documentos'
]