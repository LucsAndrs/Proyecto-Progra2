import tkinter as tk
from importlib import import_module
from tkinter import messagebox, ttk

class MainWindow(tk.Tk):
    def __init__(self, servicio=None):
        super().__init__()

        self.servicio = servicio
        self.vistas = {}

        self.title("Sistema de gestión de estacionamiento")
        self.geometry("1150x700")
        self.minsize(950, 600)
        self.protocol("WM_DELETE_WINDOW", self._confirmar_salida)

        self._configurar_estilos()
        self._crear_interfaz()
        self._crear_vistas()
        self._mostrar_vista("vehiculos")

    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure(
            "Contenedor.TFrame",
            background="#f1f5f9"
        )

        estilo.configure(
            "Titulo.TLabel",
            background="#f1f5f9",
            foreground="#0f172a",
            font=("Arial", 23, "bold")
        )

        estilo.configure(
            "Subtitulo.TLabel",
            background="#f1f5f9",
            foreground="#64748b",
            font=("Arial", 11)
        )

        estilo.configure(
            "Accion.TButton",
            font=("Arial", 10, "bold"),
            padding=9
        )

        estilo.configure(
            "Treeview",
            font=("Arial", 10),
            rowheight=28
        )

        estilo.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

    def _crear_interfaz(self):
        self.menu_lateral = tk.Frame(
            self,
            bg="#1e293b",
            width=220
        )
        self.menu_lateral.pack(
            side="left",
            fill="y"
        )
        self.menu_lateral.pack_propagate(False)

        titulo_menu = tk.Label(
            self.menu_lateral,
            text="ESTACIONAMIENTO",
            bg="#1e293b",
            fg="white",
            font=("Arial", 15, "bold"),
            pady=25
        )
        titulo_menu.pack(fill="x")

        opciones = [
            ("Vehículos", "vehiculos"),
            ("Ingresos", "ingresos"),
            ("Salidas", "salidas"),
            ("Mensualidades", "suscripciones"),
            ("Historial", "historial"),
            ("Recaudación", "reportes")
        ]

        for texto, nombre_vista in opciones:
            boton = tk.Button(
                self.menu_lateral,
                text=texto,
                command=lambda nombre=nombre_vista: self._mostrar_vista(nombre),
                bg="#1e293b",
                fg="#e2e8f0",
                activebackground="#334155",
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=25,
                pady=13,
                font=("Arial", 11),
                cursor="hand2"
            )
            boton.pack(fill="x")

        boton_salir = tk.Button(
            self.menu_lateral,
            text="Salir",
            command=self._confirmar_salida,
            bg="#991b1b",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            relief="flat",
            font=("Arial", 11, "bold"),
            pady=11,
            cursor="hand2"
        )
        boton_salir.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )

        self.contenedor = ttk.Frame(
            self,
            style="Contenedor.TFrame"
        )
        self.contenedor.pack(
            side="right",
            fill="both",
            expand=True
        )

    def _crear_vistas(self):
        secciones = [
            ("vehiculos", "Vehículos", "VehiculosView"),
            ("ingresos", "Ingresos", "IngresosView"),
            ("salidas", "Salidas", "SalidasView"),
            ("suscripciones", "Mensualidades", "SuscripcionesView"),
            ("historial", "Historial", "HistorialView"),
            ("reportes", "Recaudación", "ReportesView")
        ]

        for nombre, titulo, clase in secciones:
            # Permite ejecutar este archivo directamente o como módulo.
            modulo = f"{__package__}.{nombre}_view" if __package__ else f"{nombre}_view"
            try:
                vista_modulo = import_module(modulo)
            except ModuleNotFoundError as error:
                # Solo se reemplazan vistas pendientes, no errores internos.
                if error.name != modulo:
                    raise
                vista = self._crear_vista_pendiente(titulo)
            else:
                vista = getattr(vista_modulo, clase)(
                    self.contenedor, self.servicio
                )

            self.vistas[nombre] = vista

        for vista in self.vistas.values():
            vista.place(
                x=0,
                y=0,
                relwidth=1,
                relheight=1
            )

    def _crear_vista_pendiente(self, titulo):
        vista = ttk.Frame(self.contenedor, style="Contenedor.TFrame")
        ttk.Label(
            vista,
            text=titulo,
            style="Titulo.TLabel"
        ).pack(anchor="w", padx=30, pady=(30, 10))
        ttk.Label(
            vista,
            text="Esta sección estará disponible en una próxima etapa.",
            style="Subtitulo.TLabel"
        ).pack(anchor="w", padx=30)
        return vista

    def _mostrar_vista(self, nombre):
        vista = self.vistas.get(nombre)

        if vista is None:
            return

        vista.tkraise()

        if hasattr(vista, "actualizar"):
            vista.actualizar()

    def actualizar_vistas(self):
        for vista in self.vistas.values():
            if hasattr(vista, "actualizar"):
                vista.actualizar()

    def _confirmar_salida(self):
        respuesta = messagebox.askyesno(
            "Cerrar aplicación",
            "¿Desea cerrar el sistema?",
            parent=self
        )

        if respuesta:
            self.destroy()


if __name__ == "__main__":
    aplicacion = MainWindow()
    aplicacion.mainloop()

