from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.pago_model import Pago


class PagoRepository:

    def __init__(self, session: Session):
        self.session = session

    def guardar(
        self,
        monto: int,
        estadia_id: int | None = None,
        suscripcion_id: int | None = None
    ) -> Pago:
        try:
            pago = Pago(
                monto=monto,
                estadia_id=estadia_id,
                suscripcion_id=suscripcion_id,
                fecha_pago=datetime.now()
            )

            self.session.add(pago)
            self.session.commit()
            self.session.refresh(pago)

            return pago

        except Exception:
            self.session.rollback()
            raise

    def listar_todos(self) -> list[Pago]:
        consulta = select(Pago).order_by(
            Pago.fecha_pago.desc()
        )

        return list(self.session.scalars(consulta).all())

    def listar_por_estadia(self, estadia_id: int) -> list[Pago]:
        consulta = select(Pago).where(
            Pago.estadia_id == estadia_id
        )

        return list(self.session.scalars(consulta).all())

    def listar_por_suscripcion(
        self,
        suscripcion_id: int
    ) -> list[Pago]:

        consulta = select(Pago).where(
            Pago.suscripcion_id == suscripcion_id
        )

        return list(self.session.scalars(consulta).all())

    def calcular_ingresos(
        self,
        fecha_inicio: datetime | None = None,
        fecha_fin: datetime | None = None
    ) -> int:

        consulta = select(
            func.coalesce(func.sum(Pago.monto), 0)
        )

        if fecha_inicio is not None:
            consulta = consulta.where(
                Pago.fecha_pago >= fecha_inicio
            )

        if fecha_fin is not None:
            consulta = consulta.where(
                Pago.fecha_pago < fecha_fin
            )

        return self.session.scalar(consulta)