
import pytest

from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.models import Vehiculo
from app.repositories import (
    VehiculoRepository,
    EstadiaRepository,
    SuscripcionRepository,
    PagoRepository
)
from app.services.estacionamiento_service import EstacionamientoService


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


def crear_vehiculo(session, patente="ABC123"):
    repo = VehiculoRepository(session)
    vehiculo = repo.guardar(patente)
    session.commit()
    return vehiculo


def test_registrar_entrada(session):
    crear_vehiculo(session)

    servicio = EstacionamientoService(session)
    estadia = servicio.registrar_entrada(
        "ABC123",
        modalidad="minuto"
    )

    assert estadia.id is not None
    assert estadia.modalidad == "minuto"
    assert estadia.fecha_salida is None


def test_rechazar_doble_entrada(session):
    crear_vehiculo(session)

    servicio = EstacionamientoService(session)

    servicio.registrar_entrada(
        "ABC123",
        modalidad="minuto"
    )

    with pytest.raises(ValueError):
        servicio.registrar_entrada(
            "ABC123",
            modalidad="diaria"
        )


def test_cobro_automatico_por_minuto(session):
    crear_vehiculo(session)

    servicio = EstacionamientoService(session)

    estadia = servicio.registrar_entrada(
        "ABC123",
        modalidad="minuto"
    )

    estadia.fecha_entrada = (
        datetime.now() - timedelta(minutes=1, seconds=10)
    )
    session.commit()

    estadia, pago = servicio.registrar_salida("ABC123")

    assert estadia.fecha_salida is not None
    assert pago is not None
    assert pago.monto == 60
    assert pago.estadia_id == estadia.id


def test_cobro_automatico_diario(session):
    crear_vehiculo(session)

    servicio = EstacionamientoService(session)

    estadia = servicio.registrar_entrada(
        "ABC123",
        modalidad="diaria"
    )

    estadia.fecha_entrada = (
        datetime.now() - timedelta(days=1, minutes=1)
    )
    session.commit()

    estadia, pago = servicio.registrar_salida("ABC123")

    assert estadia.fecha_salida is not None
    assert pago is not None
    assert pago.monto == 10000
    assert pago.estadia_id == estadia.id


def test_suscripcion_cubre_estadia_despues_de_vencer(session):
    crear_vehiculo(session)

    suscripciones = SuscripcionRepository(session)
    pagos = PagoRepository(session)

    inicio = datetime.now() - timedelta(days=1)
    fin = datetime.now() + timedelta(days=30)

    suscripcion = suscripciones.guardar(
        vehiculo_id=1,
        fecha_inicio=inicio,
        fecha_fin=fin
    )

    pagos.guardar(
        monto=60000,
        suscripcion_id=suscripcion.id
    )
    session.commit()

    servicio = EstacionamientoService(session)
    estadia = servicio.registrar_entrada("ABC123")

    assert estadia.suscripcion_id == suscripcion.id

    # Simular vencimiento despues de la entrada.
    suscripcion.fecha_fin = datetime.now() - timedelta(seconds=1)
    session.commit()

    cantidad_pagos_antes = len(pagos.listar_todos())

    estadia, pago = servicio.registrar_salida("ABC123")

    cantidad_pagos_despues = len(pagos.listar_todos())

    assert estadia.fecha_salida is not None
    assert pago is None
    assert cantidad_pagos_antes == cantidad_pagos_despues


def test_rollback_si_falla_el_pago(session):
    crear_vehiculo(session)

    servicio = EstacionamientoService(session)
    estadia = servicio.registrar_entrada(
        "ABC123",
        modalidad="minuto"
    )

    def pago_fallido(*args, **kwargs):
        raise RuntimeError("Error simulado.")

    servicio.pagos.guardar = pago_fallido

    with pytest.raises(RuntimeError):
        servicio.registrar_salida("ABC123")

    session.expire_all()

    repo = EstadiaRepository(session)
    activa = repo.obtener_activa_por_vehiculo(1)

    assert activa is not None
    assert activa.id == estadia.id
    assert activa.fecha_salida is None
