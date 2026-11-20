
from datetime import datetime, timedelta

import pytest

from app.processing.tarifas import (
    calcular_cobro_minuto,
    calcular_cobro_diario,
    calcular_cobro_estadia
)


def test_cobro_minuto_y_fraccion():
    entrada = datetime(2026, 11, 20, 10, 0, 0)
    salida = entrada + timedelta(minutes=1, seconds=10)

    assert calcular_cobro_minuto(entrada, salida) == 60


def test_cobro_minimo_un_minuto():
    entrada = datetime(2026, 11, 20, 10, 0, 0)

    assert calcular_cobro_minuto(entrada, entrada) == 30


def test_cobro_minuto_exacto():
    entrada = datetime(2026, 11, 20, 10, 0, 0)
    salida = entrada + timedelta(minutes=5)

    assert calcular_cobro_minuto(entrada, salida) == 150


def test_cobro_diario_exacto():
    entrada = datetime(2026, 11, 20, 10, 0, 0)
    salida = entrada + timedelta(days=1)

    assert calcular_cobro_diario(entrada, salida) == 5000


def test_cobro_diario_con_fraccion():
    entrada = datetime(2026, 11, 20, 10, 0, 0)
    salida = entrada + timedelta(days=1, minutes=1)

    assert calcular_cobro_diario(entrada, salida) == 10000


def test_seleccion_modalidad_minuto():
    entrada = datetime(2026, 11, 20, 10, 0, 0)
    salida = entrada + timedelta(minutes=2)

    assert calcular_cobro_estadia(
        "minuto",
        entrada,
        salida
    ) == 60


def test_seleccion_modalidad_diaria():
    entrada = datetime(2026, 11, 20, 10, 0, 0)
    salida = entrada + timedelta(days=1)

    assert calcular_cobro_estadia(
        "diaria",
        entrada,
        salida
    ) == 5000


def test_rechazar_modalidad_invalida():
    entrada = datetime(2026, 11, 20, 10, 0, 0)
    salida = entrada + timedelta(minutes=5)

    with pytest.raises(ValueError):
        calcular_cobro_estadia("semanal", entrada, salida)


def test_rechazar_salida_anterior_a_entrada():
    entrada = datetime(2026, 11, 20, 10, 0, 0)
    salida = entrada - timedelta(minutes=1)

    with pytest.raises(ValueError):
        calcular_cobro_minuto(entrada, salida)
