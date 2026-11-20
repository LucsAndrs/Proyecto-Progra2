from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    patente: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True
    )

    # Relaciones con las estadías y suscripciones
    estadias: Mapped[list["Estadia"]] = relationship(
        back_populates="vehiculo"
    )

    suscripciones: Mapped[list["Suscripcion"]] = relationship(
        back_populates="vehiculo"
    )

    def __repr__(self):
        return f"Vehiculo(id={self.id}, patente='{self.patente}')"