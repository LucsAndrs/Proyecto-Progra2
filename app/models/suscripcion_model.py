from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Suscripcion(Base):
    __tablename__ = "suscripciones"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    vehiculo_id: Mapped[int] = mapped_column(
        ForeignKey("vehiculos.id"),
        nullable=False
    )

    fecha_inicio: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    fecha_fin: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    # Relación con el vehículo
    vehiculo: Mapped["Vehiculo"] = relationship(
        back_populates="suscripciones"
    )
    
    pagos: Mapped[list["Pago"]] = relationship(
    back_populates="suscripcion"
    )
    
    def __repr__(self):
        return (
            f"Suscripcion(id={self.id}, "
            f"vehiculo_id={self.vehiculo_id}, "
            f"inicio={self.fecha_inicio}, "
            f"fin={self.fecha_fin})"
        )