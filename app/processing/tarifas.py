
from datetime import datetime, timedelta


# Tarifas acordadas por el equipo (CLP).
TARIFA_POR_MINUTO = 30
TARIFA_DIARIA = 5000
TARIFA_MENSUAL = 60000


def calcular_cobro_minuto(
    fecha_entrada: datetime,
    fecha_salida: datetime
) -> int:
    if fecha_salida < fecha_entrada:
        raise ValueError("La salida no puede ser anterior a la entrada.")

    duracion = fecha_salida - fecha_entrada
    unidad = timedelta(minutes=1)

    minutos = max(
        1,
        duracion // unidad + (duracion % unidad != timedelta(0))
    )

    return minutos * TARIFA_POR_MINUTO


def calcular_cobro_diario(
    fecha_entrada: datetime,
    fecha_salida: datetime
) -> int:
    if fecha_salida < fecha_entrada:
        raise ValueError("La salida no puede ser anterior a la entrada.")

    duracion = fecha_salida - fecha_entrada
    unidad = timedelta(days=1)

    dias = max(
        1,
        duracion // unidad + (duracion % unidad != timedelta(0))
    )

    return dias * TARIFA_DIARIA


def calcular_cobro_estadia(
    modalidad: str,
    fecha_entrada: datetime,
    fecha_salida: datetime
) -> int:

    if modalidad == "minuto":
        return calcular_cobro_minuto(fecha_entrada, fecha_salida)

    if modalidad == "diaria":
        return calcular_cobro_diario(fecha_entrada, fecha_salida)

    raise ValueError("La modalidad de cobro no es valida.")
