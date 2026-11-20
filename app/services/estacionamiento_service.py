
from datetime import datetime
from app.processing.tarifas import calcular_cobro_estadia
from app.repositories import (
    VehiculoRepository,
    EstadiaRepository,
    SuscripcionRepository,
    PagoRepository
)


class EstacionamientoService:

    def __init__(self, session):
        self.session = session

        self.vehiculos = VehiculoRepository(session)
        self.estadias = EstadiaRepository(session)
        self.suscripciones = SuscripcionRepository(session)
        self.pagos = PagoRepository(session)

    def registrar_entrada(
        self,
        patente: str,
        modalidad: str | None = None
    ):
        try:
            vehiculo = self.vehiculos.obtener_por_patente(patente)

            if vehiculo is None:
                raise ValueError("El vehiculo no esta registrado.")

            estadia_activa = self.estadias.obtener_activa_por_vehiculo(
                vehiculo.id
            )

            if estadia_activa is not None:
                raise ValueError(
                    "El vehiculo ya tiene una estadia activa."
                )

            fecha_entrada = datetime.now()

            suscripcion = self.suscripciones.obtener_vigente(
                vehiculo.id,
                fecha_actual=fecha_entrada
            )

            if suscripcion is not None:
                # La suscripcion cubre la estadia.
                suscripcion_id = suscripcion.id
                modalidad = None
            else:
                # Los vehiculos sin suscripcion deben elegir modalidad.
                if modalidad not in ("minuto", "diaria"):
                    raise ValueError(
                        "Debe seleccionar modalidad minuto o diaria."
                    )

                suscripcion_id = None

            estadia = self.estadias.registrar_entrada(
                vehiculo_id=vehiculo.id,
                suscripcion_id=suscripcion_id,
                fecha_entrada=fecha_entrada,
                modalidad=modalidad
            )

            self.session.commit()

            return estadia

        except Exception:
            self.session.rollback()
            raise



    def registrar_salida(self, patente: str):
        try:
            vehiculo = self.vehiculos.obtener_por_patente(patente)

            if vehiculo is None:
                raise ValueError("El vehiculo no esta registrado.")

            estadia = self.estadias.obtener_activa_por_vehiculo(
                vehiculo.id
            )

            if estadia is None:
                raise ValueError(
                    "El vehiculo no tiene una estadia activa."
                )

            # Registrar la hora exacta de salida.
            estadia = self.estadias.registrar_salida(estadia)

            # Si tiene suscripcion asociada, no genera otro pago.
            if estadia.suscripcion_id is not None:
                self.session.commit()
                return estadia, None

            # Calcular automaticamente el cobro.
            monto = calcular_cobro_estadia(
                modalidad=estadia.modalidad,
                fecha_entrada=estadia.fecha_entrada,
                fecha_salida=estadia.fecha_salida
            )

            # Registrar el pago calculado.
            pago = self.pagos.guardar(
                monto=monto,
                estadia_id=estadia.id
            )

            self.session.commit()

            return estadia, pago

        except Exception:
            self.session.rollback()
            raise
