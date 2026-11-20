from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Pago(Base):
    __tablename__ = "pagos"

    __table_args__ = (
        CheckConstraint(
            "monto > 0",
            name="ck_pago_monto_positivo"
        ),
        CheckConstraint(
            "(estadia_id IS NOT NULL AND suscripcion_id IS NULL) "
            "OR (estadia_id IS NULL AND suscripcion_id IS NOT NULL)",
            name="ck_pago_asociacion"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    estadia_id: Mapped[int | None] = mapped_column(
        ForeignKey("estadias.id"),
        nullable=True
    )

    suscripcion_id: Mapped[int | None] = mapped_column(
        ForeignKey("suscripciones.id"),
        nullable=True
    )

    monto: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    fecha_pago: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now
    )

    # Relaciones con estadía y suscripción
    estadia: Mapped["Estadia | None"] = relationship(
        back_populates="pagos"
    )

    suscripcion: Mapped["Suscripcion | None"] = relationship(
        back_populates="pagos"
    )

    def __repr__(self):
        return (
            f"Pago(id={self.id}, "
            f"monto={self.monto}, "
            f"fecha_pago={self.fecha_pago})"
        )