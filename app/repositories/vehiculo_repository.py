from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.vehiculo_model import Vehiculo


class VehiculoRepository:

    def __init__(self, session: Session):
        self.session = session

    def guardar(self, patente: str) -> Vehiculo:
        try:
            vehiculo = Vehiculo(patente=patente.upper())

            self.session.add(vehiculo)
            self.session.commit()
            self.session.refresh(vehiculo)

            return vehiculo

        except Exception:
            self.session.rollback()
            raise

    def obtener_por_id(self, vehiculo_id: int) -> Vehiculo | None:
        return self.session.get(Vehiculo, vehiculo_id)

    def obtener_por_patente(self, patente: str) -> Vehiculo | None:
        consulta = select(Vehiculo).where(
            Vehiculo.patente == patente.upper()
        )

        return self.session.scalar(consulta)

    def listar_todos(self) -> list[Vehiculo]:
        consulta = select(Vehiculo).order_by(Vehiculo.id)

        return list(self.session.scalars(consulta).all())