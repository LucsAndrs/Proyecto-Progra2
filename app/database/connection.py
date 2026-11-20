from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base


# Ubicación de la base de datos
DATABASE_URL = "sqlite:///./data/estacionamiento.db"


# Crear el motor de conexión
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Crear sesiones para interactuar con la base de datos
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# Crear las tablas registradas en Base
def crear_tablas():
    Base.metadata.create_all(bind=engine)