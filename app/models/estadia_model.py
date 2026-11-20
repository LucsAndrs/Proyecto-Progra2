from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Estadia(Base):
    __tablename__ = "estadias"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    vehiculo_id: Mapped[int] = mapped_column(
        ForeignKey("vehiculos.id"),
        nullable=False
    )

    fecha_entrada: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    fecha_salida: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    # Relación con el vehículo
    vehiculo: Mapped["Vehiculo"] = relationship(
        back_populates="estadias"
    )
    
    pagos: Mapped[list["Pago"]] = relationship(
    back_populates="estadia"
    )
    
    def __repr__(self):
        return (
            f"Estadia(id={self.id}, "
            f"vehiculo_id={self.vehiculo_id}, "
            f"entrada={self.fecha_entrada}, "
            f"salida={self.fecha_salida})"
        )