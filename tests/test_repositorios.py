
import pytest

from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.models import Vehiculo, Estadia, Suscripcion, Pago
from app.repositories import (
    VehiculoRepository,
    EstadiaRepository,
    SuscripcionRepository,
    PagoRepository
)


@pytest.fixture
def session():
    # Crear una base de datos temporal en memoria.
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )

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


def test_guardar_y_obtener_vehiculo(session):
    repo = VehiculoRepository(session)

    vehiculo = repo.guardar("ABC123")

    resultado = repo.obtener_por_patente("ABC123")

    assert resultado is not None
    assert resultado.id == vehiculo.id
    assert resultado.patente == "ABC123"


def test_listar_vehiculos(session):
    repo = VehiculoRepository(session)

    repo.guardar("ABC123")
    repo.guardar("DEF456")

    resultado = repo.listar_todos()

    assert len(resultado) == 2


def test_registrar_y_consultar_estadia_activa(session):
    vehiculos = VehiculoRepository(session)
    estadias = EstadiaRepository(session)

    vehiculo = vehiculos.guardar("ABC123")

    estadia = estadias.registrar_entrada(
        vehiculo_id=vehiculo.id,
        modalidad="minuto"
    )

    resultado = estadias.obtener_activa_por_vehiculo(
        vehiculo.id
    )

    assert resultado is not None
    assert resultado.id == estadia.id
    assert resultado.fecha_salida is None
    assert resultado.modalidad == "minuto"


def test_registrar_salida_de_estadia(session):
    vehiculos = VehiculoRepository(session)
    estadias = EstadiaRepository(session)

    vehiculo = vehiculos.guardar("ABC123")

    estadia = estadias.registrar_entrada(
        vehiculo_id=vehiculo.id,
        modalidad="diaria"
    )

    estadias.registrar_salida(estadia)

    resultado = estadias.obtener_activa_por_vehiculo(
        vehiculo.id
    )

    assert resultado is None
    assert estadia.fecha_salida is not None


def test_guardar_y_consultar_suscripcion(session):
    vehiculos = VehiculoRepository(session)
    suscripciones = SuscripcionRepository(session)

    vehiculo = vehiculos.guardar("ABC123")

    inicio = datetime.now()
    fin = inicio + timedelta(days=30)

    suscripcion = suscripciones.guardar(
        vehiculo_id=vehiculo.id,
        fecha_inicio=inicio,
        fecha_fin=fin
    )

    resultado = suscripciones.obtener_vigente(
        vehiculo.id,
        fecha_actual=inicio + timedelta(days=1)
    )

    assert resultado is not None
    assert resultado.id == suscripcion.id


def test_guardar_pago_y_calcular_ingresos(session):
    vehiculos = VehiculoRepository(session)
    estadias = EstadiaRepository(session)
    pagos = PagoRepository(session)

    vehiculo = vehiculos.guardar("ABC123")

    estadia = estadias.registrar_entrada(
        vehiculo_id=vehiculo.id,
        modalidad="minuto"
    )

    pagos.guardar(
        monto=60,
        estadia_id=estadia.id
    )

    pagos.guardar(
        monto=90,
        estadia_id=estadia.id
    )

    total = pagos.calcular_ingresos()

    assert total == 150
    assert len(pagos.listar_por_estadia(estadia.id)) == 2
