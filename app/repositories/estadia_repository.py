
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.estadia_model import Estadia


class EstadiaRepository:

    def __init__(self, session: Session):
        self.session = session

    def registrar_entrada(
        self,
        vehiculo_id: int,
        suscripcion_id: int | None = None,
        fecha_entrada: datetime | None = None,
        modalidad: str | None = None
    ) -> Estadia:

        if fecha_entrada is None:
            fecha_entrada = datetime.now()

        estadia = Estadia(
            vehiculo_id=vehiculo_id,
            suscripcion_id=suscripcion_id,
            fecha_entrada=fecha_entrada,
            modalidad=modalidad
        )

        self.session.add(estadia)
        self.session.flush()
        self.session.refresh(estadia)

        return estadia

    def registrar_salida(self, estadia: Estadia) -> Estadia:
        estadia.fecha_salida = datetime.now()

        self.session.flush()
        self.session.refresh(estadia)

        return estadia

    def obtener_activa_por_vehiculo(
        self,
        vehiculo_id: int
    ) -> Estadia | None:

        consulta = select(Estadia).where(
            Estadia.vehiculo_id == vehiculo_id,
            Estadia.fecha_salida.is_(None)
        )

        return self.session.scalar(consulta)

    def listar_activas(self) -> list[Estadia]:
        consulta = select(Estadia).where(
            Estadia.fecha_salida.is_(None)
        )

        return list(self.session.scalars(consulta).all())

    def listar_todas(self) -> list[Estadia]:
        consulta = select(Estadia).order_by(
            Estadia.fecha_entrada.desc()
        )

        return list(self.session.scalars(consulta).all())
