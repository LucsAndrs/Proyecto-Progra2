from datetime import datetime, timedelta
from app.processing.tarifas import TARIFA_MENSUAL
from app.repositories import (
    VehiculoRepository,
    SuscripcionRepository,
    PagoRepository
)


class SuscripcionService:

    def __init__(self, session):
        self.session = session

        self.vehiculos = VehiculoRepository(session)
        self.suscripciones = SuscripcionRepository(session)
        self.pagos = PagoRepository(session)


    def contratar(
        self,
        patente: str,
    ):
        try:
            vehiculo = self.vehiculos.obtener_por_patente(patente)

            if vehiculo is None:
                raise ValueError("El vehiculo no esta registrado.")

            fecha_inicio = datetime.now()
            fecha_fin = fecha_inicio + timedelta(days=30)

            # Comprobar cualquier periodo que se superponga.
            existe_solapamiento = (
                self.suscripciones.existe_solapamiento(
                    vehiculo_id=vehiculo.id,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin
                )
            )

            if existe_solapamiento:
                raise ValueError(
                    "El vehiculo ya tiene una suscripcion "
                    "con un periodo superpuesto."
                )

            suscripcion = self.suscripciones.guardar(
                vehiculo_id=vehiculo.id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )

            pago = self.pagos.guardar(
                monto=TARIFA_MENSUAL,
                suscripcion_id=suscripcion.id
            )

            self.session.commit()

            return suscripcion, pago

        except Exception:
            self.session.rollback()
            raise
