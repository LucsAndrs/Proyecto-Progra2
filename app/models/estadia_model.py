
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String
from app.database.base import Base


class Estadia(Base):
    __tablename__ = "estadias"
    __table_args__ = (
        CheckConstraint(
            "modalidad IS NULL OR modalidad IN ('minuto', 'diaria')",
            name="ck_estadia_modalidad"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    vehiculo_id: Mapped[int] = mapped_column(
        ForeignKey("vehiculos.id"),
        nullable=False
    )

    modalidad: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    suscripcion_id: Mapped[int | None] = mapped_column(
        ForeignKey("suscripciones.id"),
        nullable=True
    )

    fecha_entrada: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    fecha_salida: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    vehiculo: Mapped["Vehiculo"] = relationship(
        back_populates="estadias"
    )

    suscripcion: Mapped["Suscripcion | None"] = relationship(
        back_populates="estadias"
    )

    pagos: Mapped[list["Pago"]] = relationship(
        back_populates="estadia"
    )

    def __repr__(self):
        return (
            f"Estadia(id={self.id}, "
            f"vehiculo_id={self.vehiculo_id}, "
            f"suscripcion_id={self.suscripcion_id}, "
            f"entrada={self.fecha_entrada}, "
            f"salida={self.fecha_salida})"
        )
