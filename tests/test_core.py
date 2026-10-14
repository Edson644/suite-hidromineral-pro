"""
Pruebas unitarias (pytest) para el módulo de Chancado.
Verifica el valor de referencia de Bond solicitado.
"""

import pytest
from core.chancado import calcular_trabajo_bond

def test_bond_calculation():
    # Bond (Wi 13,5; F80 50.000 µm; P80 12.000 µm) = 0,63 kWh/t aprox.
    wi = 13.5
    f80 = 50000.0
    p80 = 12000.0
    tonelaje = 100.0
    res = calcular_trabajo_bond(wi, f80, p80, tonelaje)
    assert pytest.approx(res["w_kwh_t"], rel=1e-2) == 0.6304

