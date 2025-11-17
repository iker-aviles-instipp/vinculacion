from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from django.urls import reverse # Necesario para usar reverse en E2E tests
from selenium.webdriver.support.ui import WebDriverWait # Importación necesaria
from selenium.webdriver.support import expected_conditions as EC # Importación necesaria
from datetime import date, time # Aunque no las uses ahora, suelen ser necesarias en E2E

class CitaE2ETest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome() 
        User.objects.create_user(username="doctor", password="12345")

    def tearDown(self):
        self.browser.quit()

    def test_login_y_agendar_cita(self):
        # 1. Navegar a Login
        self.browser.get(self.live_server_url + reverse('login'))
        
        # 2. Rellenar credenciales
        self.browser.find_element(By.NAME, "username").send_keys("doctor")
        self.browser.find_element(By.NAME, "password").send_keys("12345")
        
        # 3. Hacer clic con espera explícita
        wait = WebDriverWait(self.browser, 10) 

        # Corrección del selector de login (mantener la versión correcta: input[type='submit'])
        login_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
        )
        login_button.click()
        
        # 4. Navegar a la página de agendar cita
        # El login exitoso probablemente lleva a /base, así que navegamos explícitamente a agendarCi
        self.browser.get(self.live_server_url + reverse('agendarCi')) 
        
        # --- 5. Verificación (CORRECCIÓN CLAVE: Verificar contenido, no el título estático) ---
        
        # Esperar a que el encabezado 'Agendar Cita' esté presente en el DOM
        try:
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Agendar Cita')]"))
            )
            # Aserción final: verificar que el texto "Agendar Cita" está en el código fuente de la página
            self.assertIn("Agendar Cita", self.browser.page_source)
        except Exception:
            self.fail(
                f"No se pudo encontrar el encabezado 'Agendar Cita' en la página. Título actual: {self.browser.title}"
            )
        # ----------------------------------------------------------------------------------------

        # --- Agregar pasos de interacción para completar la prueba E2E ---
        
        # Rellenar formulario (Ejemplo: crea un paciente nuevo)
        
        # Nota: Asegúrate que el campo cédula en agendarCi.html tenga name="cedula"
        self.browser.find_element(By.NAME, "cedula").send_keys("1234567890")
        self.browser.find_element(By.NAME, "nombre").send_keys("Paciente")
        self.browser.find_element(By.NAME, "apellido").send_keys("Test")
        self.browser.find_element(By.NAME, "fecha").send_keys("2025-12-25")
        self.browser.find_element(By.NAME, "hora").send_keys("14:30")
        self.browser.find_element(By.NAME, "motivo").send_keys("Revision y limpieza")

        # Hacer clic en el botón 'Agendar' (que es un botón <button>)
        self.browser.find_element(By.XPATH, "//button[text()='Agendar']").click()
        
        # Opcional: Verificar mensaje de éxito
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))
        
        # -----------------------------------------------------------------------------