from datetime import datetime

from app.repositories import (
    VehiculoRepository,
    EstadiaRepository,
    PagoRepository
)

from app.processing.funciones import (
    obtener_patentes,
    filtrar_estadias_activas,
    filtrar_pagos_por_periodo,
    calcular_total_ingresos
)


class Reportes:

    def __init__(
        self,
        vehiculos: VehiculoRepository,
        estadias: EstadiaRepository,
        pagos: PagoRepository
    ):
        self.vehiculos = vehiculos
        self.estadias = estadias
        self.pagos = pagos

    def generar_resumen(self) -> dict:
        lista_vehiculos = self.vehiculos.listar_todos()
        lista_estadias = self.estadias.listar_todas()
        lista_pagos = self.pagos.listar_todos()

        activas = filtrar_estadias_activas(lista_estadias)

        return {
            "total_vehiculos": len(lista_vehiculos),
            "patentes": obtener_patentes(lista_vehiculos),
            "total_estadias": len(lista_estadias),
            "estadias_activas": len(activas),
            "total_pagos": len(lista_pagos),
            "ingresos_totales": calcular_total_ingresos(lista_pagos)
        }

    def generar_reporte_ingresos(
        self,
        fecha_inicio: datetime | None = None,
        fecha_fin: datetime | None = None
    ) -> dict:

        lista_pagos = self.pagos.listar_todos()

        pagos_filtrados = filtrar_pagos_por_periodo(
            lista_pagos,
            fecha_inicio,
            fecha_fin
        )

        return {
            "cantidad_pagos": len(pagos_filtrados),
            "ingresos_totales": calcular_total_ingresos(
                pagos_filtrados
            ),
            "pagos": pagos_filtrados
        }