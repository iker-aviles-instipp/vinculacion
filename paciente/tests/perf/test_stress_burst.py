import os
import math
import time
import requests
import pytest
from django.urls import reverse # Necesario para obtener la URL de login
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- Configuración con Variables de Entorno (Valores por defecto) ---
USERS = int(os.getenv("BURST_USERS", "20"))        # 20 hilos concurrentes
REQUESTS = int(os.getenv("BURST_REQUESTS", "100"))  # 100 requests en total
P95_MS = int(os.getenv("P95_MS", "2500"))          # Umbral P95: 2500 ms (2.5 segundos)
ERROR_RATE_MAX = float(os.getenv("ERROR_RATE_MAX", "0.05")) # Tasa de error máxima: 5%


def percentile(values, p):
    """Retorna el percentil p (0-100) de una lista no vacía."""
    if not values:
        return math.nan
    values = sorted(values)
    k = (len(values)-1) * (p/100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return values[int(k)]
    # Interpolación lineal simple
    return values[f] + (values[c] - values[f]) * (k - f)


@pytest.mark.perf
def test_burst_stress_login(live_server):
    """
    Ráfaga concurrente de requests (GET) al login para medir estabilidad.
    """
    
    # --- ADAPTACIÓN CLAVE: Obtener la URL de login ---
    # Asumo que el nombre de tu vista de login en urls.py es 'login'.
    login_url_path = reverse('login')
    url = f"{live_server.url}{login_url_path}"

    print(f"\n--- Burst Test ---")
    print(f"URL: {url}")
    print(f"Concurrent Users (Threads): {USERS}")
    print(f"Total Requests: {REQUESTS}")
    print(f"SLA P95: {P95_MS} ms | Max Error Rate: {ERROR_RATE_MAX:.1%}")
    # ------------------------------------------------

    latencies = []
    errors = 0

    def shoot(_):
        """Función que realiza un solo request y mide la latencia."""
        t0 = time.perf_counter()
        try:
            # Timeout para la solicitud de 5 segundos
            r = requests.get(url, timeout=5) 
            # Se considera OK si el status está en el rango 2xx o 3xx
            ok = (200 <= r.status_code < 400) 
        except Exception:
            # Error de conexión o timeout
            ok = False
        dt = (time.perf_counter() - t0) * 1000
        return ok, dt

    with ThreadPoolExecutor(max_workers=USERS) as ex:
        futures = [ex.submit(shoot, i) for i in range(REQUESTS)]
        for fut in as_completed(futures):
            ok, ms = fut.result()
            if ok:
                latencies.append(ms)
            else:
                errors += 1

    total = REQUESTS
    error_rate = errors / total
    
    # Cálculo de métricas
    p95 = percentile(latencies, 95) if latencies else float("inf")
    avg = sum(latencies) / len(latencies) if latencies else float("inf")

    print(f"Results: Avg={avg:.1f} ms | P95={p95:.1f} ms | Errors={errors}")
    
    # --- Assertions (Verificaciones Funcionales y No Funcionales) ---
    
    # 1. Tasa de error (funcionalidad y estabilidad)
    assert error_rate <= ERROR_RATE_MAX, f"FALLO: Tasa de error {error_rate:.1%} > {ERROR_RATE_MAX:.1%} (Errores: {errors}/{total})"
    
    # 2. Latencia P95 (rendimiento)
    assert p95 <= P95_MS, f"FALLO: P95 {p95:.1f} ms > {P95_MS} ms (Latencia promedio: {avg:.1f} ms)"