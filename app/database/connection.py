from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.database.base import Base


DATABASE_URL = "sqlite:///./data/estacionamiento.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def obtener_sesion() -> Session:
    return SessionLocal()


def crear_tablas():
    Base.metadata.create_all(bind=engine)