from django.test import TestCase
from paciente.models import Pacientes, cita
from datetime import date, time

class PacientesModelTest(TestCase):
    def test_crear_paciente(self):
        paciente = Pacientes.objects.create(
            nombre="Carlos",
            apellido="Ramírez",
            cedula="0701234567",
            direccion="Machala",
            celular="0998765432",
            fecha_nacimiento=date(1990, 5, 10),
            estado_civil="Soltero",
            edad=33,
            correo="carlos@gmail.com",
            tipo_sangre="O+",
            fecha_cita=date(2025, 11, 10),
            hora_cita=time(10, 30),
            tipo_tratamiento="Limpieza dental"
        )
        self.assertEqual(paciente.nombre, "Carlos")
        self.assertEqual(str(paciente.apellido), "Ramírez")

class CitaModelTest(TestCase):
    def test_crear_cita(self):
        paciente = Pacientes.objects.create(
            nombre="Ana", apellido="Lopez", cedula="0709876543",
            direccion="Centro", celular="0987654321",
            fecha_nacimiento=date(1995, 7, 2), estado_civil="Casada",
            edad=29, correo="ana@gmail.com", tipo_sangre="A+",
            fecha_cita=date(2025, 11, 9), hora_cita=time(11, 0),
            tipo_tratamiento="Ortodoncia"
        )
        nueva_cita = cita.objects.create(
            paciente=paciente,
            fecha_cita=date(2025, 11, 10),
            hora_cita=time(9, 0),
            tipo_tratamiento="Limpieza dental"
        )
        self.assertEqual(str(nueva_cita), "Cita de Ana Lopez para el 2025-11-10 a las 09:00:00")