import time
import requests
import pytest
from django.urls import reverse

# Asegúrate de tener Pytest y requests instalados: 
# pip install pytest requests pytest-django

def test_login_latency_detailed(live_server):
    """
    Mide el tiempo total de respuesta y el Time To First Byte (TTFB) 
    para la página de inicio de sesión.
    """
    
    # Adaptación: Usar reverse('nombre_de_la_vista_login') para construir la URL de forma segura.
    # Asumo que el nombre de tu vista de login en urls.py es 'login'. Si es otro, cámbialo.
    login_url_path = reverse('login') 
    url = f"{live_server.url}{login_url_path}"

    print(f"\nProbando URL: {url}")
    
    # Medición DNS + Conexión + Transferencia
    t0 = time.perf_counter()
    # Usar un timeout de 10 segundos para evitar que el test se cuelgue.
    try:
        resp = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        pytest.fail(f"La solicitud a {url} ha excedido el tiempo de espera (10s)")
        
    total_time = (time.perf_counter() - t0) * 1000

    # Tiempo hasta primer byte (TTFB)
    # resp.elapsed proporciona el objeto timedelta, total_seconds() lo convierte a segundos.
    ttfb = resp.elapsed.total_seconds() * 1000

    print(f"\n=== DIAGNÓSTICO DETALLADO ===")
    print(f"Tiempo total (latencia): {total_time:.1f} ms")
    print(f"TTFB (Time To First Byte): {ttfb:.1f} ms")
    # Nota: El tiempo de transferencia es la diferencia entre total_time y ttfb
    print(f"Tiempo de Transferencia: {total_time - ttfb:.1f} ms")
    print(f"Tamaño respuesta: {len(resp.content)} bytes")
    print(f"Headers: {dict(resp.headers)}")

    # Verificación de que la solicitud fue exitosa
    assert resp.status_code == 200, f"Se esperaba un código 200, se recibió {resp.status_code}"