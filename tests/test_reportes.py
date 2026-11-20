
import pytest

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.repositories import (
    VehiculoRepository,
    EstadiaRepository,
    PagoRepository
)
from app.processing.reportes import Reportes


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(bind=engine)

    TestingSession = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False
    )

    db = TestingSession()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def preparar_reportes(session):
    vehiculos = VehiculoRepository(session)
    estadias = EstadiaRepository(session)
    pagos = PagoRepository(session)

    # Registrar dos vehiculos.
    vehiculo1 = vehiculos.guardar("ABC123")
    vehiculo2 = vehiculos.guardar("DEF456")

    # Registrar dos estadias.
    estadia1 = estadias.registrar_entrada(
        vehiculo1.id,
        modalidad="minuto"
    )

    estadia2 = estadias.registrar_entrada(
        vehiculo2.id,
        modalidad="diaria"
    )

    # Cerrar la segunda estadia.
    estadias.registrar_salida(estadia2)

    # Registrar dos pagos.
    pago1 = pagos.guardar(
        monto=60,
        estadia_id=estadia1.id
    )

    pago2 = pagos.guardar(
        monto=90,
        estadia_id=estadia2.id
    )

    # Asignar fechas controladas a los pagos.
    pago1.fecha_pago = datetime(2026, 11, 20, 10, 0)
    pago2.fecha_pago = datetime(2026, 11, 21, 10, 0)

    session.commit()

    return Reportes(vehiculos, estadias, pagos)


def test_generar_resumen_general(session):
    reportes = preparar_reportes(session)

    resultado = reportes.generar_resumen()

    assert resultado["total_vehiculos"] == 2
    assert resultado["patentes"] == ["ABC123", "DEF456"]
    assert resultado["total_estadias"] == 2
    assert resultado["estadias_activas"] == 1
    assert resultado["total_pagos"] == 2
    assert resultado["ingresos_totales"] == 150


def test_generar_reporte_ingresos_por_periodo(session):
    reportes = preparar_reportes(session)

    inicio = datetime(2026, 11, 20, 0, 0)
    fin = datetime(2026, 11, 21, 0, 0)

    resultado = reportes.generar_reporte_ingresos(
        fecha_inicio=inicio,
        fecha_fin=fin
    )

    assert resultado["cantidad_pagos"] == 1
    assert resultado["ingresos_totales"] == 60
    assert len(resultado["pagos"]) == 1


def test_generar_reporte_sin_pagos_en_periodo(session):
    reportes = preparar_reportes(session)

    inicio = datetime(2026, 11, 22, 0, 0)
    fin = datetime(2026, 11, 23, 0, 0)

    resultado = reportes.generar_reporte_ingresos(
        fecha_inicio=inicio,
        fecha_fin=fin
    )

    assert resultado["cantidad_pagos"] == 0
    assert resultado["ingresos_totales"] == 0
    assert resultado["pagos"] == []
