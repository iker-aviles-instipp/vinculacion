from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, time
from paciente.models import Pacientes, cita

class LoginAndCitaIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="admin", password="12345")
        
        # CORRECCIÓN CLAVE: Proporcionar valores para todos los campos NOT NULL 
        # en el modelo Pacientes, incluso si son datos de cita.
        self.paciente = Pacientes.objects.create(
            nombre="Mario", apellido="Torres", cedula="0701122334",
            direccion="Av. Las Palmeras", celular="0981234567",
            fecha_nacimiento=date(1993, 4, 5), estado_civil="Soltero",
            edad=31, correo="mario@gmail.com", tipo_sangre="B+",
            
            # --- CAMPOS OBLIGATORIOS (NOT NULL) DE PACIENTES ---
            fecha_cita=date.today(),       # Solución del error anterior
            hora_cita=time(12, 0),         # <-- SOLUCIÓN para el error actual
            tipo_tratamiento="Inicial",    # <-- Posiblemente obligatorio también
            # ----------------------------------------------------
        )
        
    def test_login_y_creacion_cita(self):
        login = self.client.login(username="admin", password="12345")
        self.assertTrue(login)
        
        # Los campos POST deben usar los nombres que tu vista espera: 'fecha', 'hora', 'motivo'
        response = self.client.post(reverse('agendarCi_guardar'), {
            # Datos del Paciente (Obligatorios para get_or_create)
            'cedula': self.paciente.cedula,  
            'nombre': self.paciente.nombre,  
            'apellido': self.paciente.apellido, 
            'celular': self.paciente.celular, 
            
            # Datos de la Cita (claves de POST que la vista espera)
            'fecha': '2025-11-12',               
            'hora': '09:30',                     
            'motivo': 'Extracción',              
        })
        
        self.assertEqual(response.status_code, 302) 

        # Verificación
        self.assertTrue(cita.objects.filter(
            paciente=self.paciente,
            fecha_cita=date(2025, 11, 12),
            hora_cita=time(9, 30),
            tipo_tratamiento='Extracción'
        ).exists())