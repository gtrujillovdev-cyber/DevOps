import pytest
from collector.monitor import collect_metrics

def test_collect_metrics():
    """
    Verifica que la función collect_metrics retorne una estructura de diccionario
    con todas las llaves obligatorias y los tipos de datos correctos.
    """
    metrics = collect_metrics()
    
    # Comprobar estructura principal
    assert isinstance(metrics, dict)
    for key in ["cpu", "ram", "disk", "network", "top_processes", "timestamp"]:
        assert key in metrics

    # Comprobar tipos de datos de métricas básicas
    assert isinstance(metrics["cpu"], (int, float))
    assert 0 <= metrics["cpu"] <= 100

    assert isinstance(metrics["ram"], (int, float))
    assert 0 <= metrics["ram"] <= 100

    assert isinstance(metrics["disk"], (int, float))
    assert 0 <= metrics["disk"] <= 100

    # Comprobar estructura de red
    assert isinstance(metrics["network"], dict)
    assert "bytes_sent" in metrics["network"]
    assert "bytes_recv" in metrics["network"]
    assert isinstance(metrics["network"]["bytes_sent"], int)
    assert isinstance(metrics["network"]["bytes_recv"], int)

    # Comprobar estructura de procesos principales
    assert isinstance(metrics["top_processes"], list)
    assert len(metrics["top_processes"]) <= 5
    for proc in metrics["top_processes"]:
        assert isinstance(proc, dict)
        assert "pid" in proc
        assert "name" in proc
        assert "cpu_percent" in proc
