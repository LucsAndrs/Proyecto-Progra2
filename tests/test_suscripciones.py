
import pytest

from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.repositories import (
    VehiculoRepository,
    SuscripcionRepository,
    PagoRepository
)
from app.services.suscripcion_service import SuscripcionService


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


def crear_vehiculo(session):
    vehiculos = VehiculoRepository(session)
    vehiculo = vehiculos.guardar("ABC123")
    session.commit()
    return vehiculo


def test_contratar_suscripcion(session):
    crear_vehiculo(session)

    servicio = SuscripcionService(session)

    suscripcion, pago = servicio.contratar("ABC123")

    assert suscripcion.id is not None
    assert suscripcion.fecha_fin - suscripcion.fecha_inicio == timedelta(days=30)
    assert pago.monto == 60000
    assert pago.suscripcion_id == suscripcion.id


def test_consultar_suscripcion_vigente(session):
    vehiculo = crear_vehiculo(session)

    servicio = SuscripcionService(session)
    suscripcion, pago = servicio.contratar("ABC123")

    repositorio = SuscripcionRepository(session)

    resultado = repositorio.obtener_vigente(
        vehiculo.id,
        fecha_actual=datetime.now()
    )

    assert resultado is not None
    assert resultado.id == suscripcion.id


def test_rechazar_segunda_suscripcion_vigente(session):
    crear_vehiculo(session)

    servicio = SuscripcionService(session)

    servicio.contratar("ABC123")

    with pytest.raises(ValueError):
        servicio.contratar("ABC123")

    pagos = PagoRepository(session)

    assert len(pagos.listar_todos()) == 1


def test_precio_suscripcion_mensual_fijo(session):
    crear_vehiculo(session)

    servicio = SuscripcionService(session)
    suscripcion, pago = servicio.contratar("ABC123")

    assert pago.monto == 60000
    assert (suscripcion.fecha_fin - suscripcion.fecha_inicio) == timedelta(days=30)


def test_rollback_si_falla_el_pago(session):
    crear_vehiculo(session)

    servicio = SuscripcionService(session)

    def pago_fallido(*args, **kwargs):
        raise RuntimeError("Error simulado.")

    servicio.pagos.guardar = pago_fallido

    with pytest.raises(RuntimeError):
        servicio.contratar("ABC123")

    session.expire_all()

    suscripciones = SuscripcionRepository(session)

    resultado = suscripciones.listar_por_vehiculo(1)

    assert resultado == []

def test_rechazar_suscripcion_futura_superpuesta(session):
    vehiculo = crear_vehiculo(session)

    repositorio = SuscripcionRepository(session)

    # Suscripcion futura que comienza dentro de 20 dias.
    inicio_futuro = datetime.now() + timedelta(days=20)
    fin_futuro = inicio_futuro + timedelta(days=30)

    repositorio.guardar(
        vehiculo_id=vehiculo.id,
        fecha_inicio=inicio_futuro,
        fecha_fin=fin_futuro
    )
    session.commit()

    servicio = SuscripcionService(session)

    # La nueva suscripcion comenzaria ahora y duraria 30 dias.
    # Por tanto, se superpondria con la futura.
    with pytest.raises(ValueError, match="periodo superpuesto"):
        servicio.contratar("ABC123")


def test_permitir_suscripcion_futura_sin_superposicion(session):
    vehiculo = crear_vehiculo(session)

    repositorio = SuscripcionRepository(session)

    # Suscripcion existente que comienza despues de 30 dias.
    inicio_futuro = datetime.now() + timedelta(days=31)
    fin_futuro = inicio_futuro + timedelta(days=30)

    repositorio.guardar(
        vehiculo_id=vehiculo.id,
        fecha_inicio=inicio_futuro,
        fecha_fin=fin_futuro
    )
    session.commit()

    servicio = SuscripcionService(session)

    # La nueva suscripcion termina antes de que comience la futura.
    suscripcion, pago = servicio.contratar("ABC123")

    assert suscripcion.id is not None
    assert pago.monto == 60000
    assert suscripcion.fecha_fin <= inicio_futuro
