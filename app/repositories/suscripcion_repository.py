from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.suscripcion_model import Suscripcion


class SuscripcionRepository:

    def __init__(self, session: Session):
        self.session = session

    def guardar(
        self,
        vehiculo_id: int,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> Suscripcion:
        try:
            suscripcion = Suscripcion(
                vehiculo_id=vehiculo_id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )

            self.session.add(suscripcion)
            self.session.commit()
            self.session.refresh(suscripcion)

            return suscripcion

        except Exception:
            self.session.rollback()
            raise

    def obtener_vigente(
        self,
        vehiculo_id: int,
        fecha_actual: datetime | None = None
    ) -> Suscripcion | None:

        if fecha_actual is None:
            fecha_actual = datetime.now()

        consulta = select(Suscripcion).where(
            Suscripcion.vehiculo_id == vehiculo_id,
            Suscripcion.fecha_inicio <= fecha_actual,
            Suscripcion.fecha_fin > fecha_actual
        ).order_by(Suscripcion.fecha_fin.desc())

        return self.session.scalar(consulta)

    def listar_por_vehiculo(
        self,
        vehiculo_id: int
    ) -> list[Suscripcion]:

        consulta = select(Suscripcion).where(
            Suscripcion.vehiculo_id == vehiculo_id
        ).order_by(Suscripcion.fecha_inicio.desc())

        return list(self.session.scalars(consulta).all())

    def listar_todas(self) -> list[Suscripcion]:
        consulta = select(Suscripcion).order_by(
            Suscripcion.fecha_inicio.desc()
        )

        return list(self.session.scalars(consulta).all())