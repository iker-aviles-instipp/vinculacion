import os
import time
import requests
import pytest
from django.urls import reverse

# Permite ajustar el SLA sin tocar el código: 
# Ejecución de ejemplo (Windows): $env:SLA_MS=500 ; pytest -m perf
# Ejecución de ejemplo (Linux/macOS): SLA_MS=500 pytest -m perf
SLA_MS = int(os.getenv("SLA_MS", 2500)) # Valor por defecto de 2000 ms (2 segundos)


@pytest.mark.perf
def test_login_page_latency_sla(live_server):
    """
    Verifica que la página de login responda por debajo del SLA (SLA_MS).
    """
    
    # Adaptación: Usar reverse() para obtener la URL de login.
    # Asumo que el nombre de tu vista de login en urls.py es 'login'.
    login_url_path = reverse('login')
    url = f"{live_server.url}{login_url_path}"

    print(f"\n--- Probando SLA: {SLA_MS} ms en {url} ---")

    t0 = time.perf_counter()
    # Usar un timeout de 5 segundos para la solicitud
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        pytest.fail(f"La solicitud a {url} ha excedido el tiempo de espera de 5s.")
        
    elapsed_ms = (time.perf_counter() - t0) * 1000

    print(f"Latencia medida: {elapsed_ms:.1f} ms")

    # 1. 200 OK
    assert resp.status_code == 200, f"Status inesperado {resp.status_code} para {url}. Contenido: {resp.text[:100]}..."
    
    # 2. Debajo del umbral SLA
    assert elapsed_ms <= SLA_MS, f"FALLO SLA: Latencia {elapsed_ms:.1f} ms excede el umbral de {SLA_MS} ms"