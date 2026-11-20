from datetime import datetime
from functools import reduce

from app.models.vehiculo_model import Vehiculo
from app.models.estadia_model import Estadia
from app.models.pago_model import Pago


# Obtener las patentes de los vehículos.
def obtener_patentes(vehiculos: list[Vehiculo]) -> list[str]:
    return list(
        map(lambda vehiculo: vehiculo.patente, vehiculos)
    )


# Obtener solamente las estadías que siguen activas.
def filtrar_estadias_activas(
    estadias: list[Estadia]
) -> list[Estadia]:

    return list(
        filter(
            lambda estadia: estadia.fecha_salida is None,
            estadias
        )
    )


# Filtrar pagos dentro de un período.
# La fecha inicial es inclusiva y la final es exclusiva.
def filtrar_pagos_por_periodo(
    pagos: list[Pago],
    fecha_inicio: datetime | None = None,
    fecha_fin: datetime | None = None
) -> list[Pago]:

    return list(
        filter(
            lambda pago: (
                (fecha_inicio is None or pago.fecha_pago >= fecha_inicio)
                and
                (fecha_fin is None or pago.fecha_pago < fecha_fin)
            ),
            pagos
        )
    )


# Calcular la suma de todos los pagos.
def calcular_total_ingresos(pagos: list[Pago]) -> int:
    return reduce(
        lambda total, pago: total + pago.monto,
        pagos,
        0
    )