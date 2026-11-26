import tkinter as tk
from tkinter import messagebox, ttk


class VehiculosView(ttk.Frame):
    def __init__(self, parent, servicio=None):
        super().__init__(parent, style="Contenedor.TFrame")

        self.servicio = servicio
        self.patente = tk.StringVar()
        self.contacto = tk.StringVar()

        self._crear_interfaz()

    def _crear_interfaz(self):
        ttk.Label(
            self,
            text="Registro de vehículos",
            style="Titulo.TLabel"
        ).pack(anchor="w", padx=30, pady=(30, 10))

        ttk.Label(
            self,
            text="Ingrese la patente y el teléfono de contacto.",
            style="Subtitulo.TLabel"
        ).pack(anchor="w", padx=30, pady=(0, 20))

        formulario = ttk.Frame(self, style="Contenedor.TFrame")
        formulario.pack(anchor="w", padx=30)

        ttk.Label(
            formulario,
            text="Patente:",
            style="Subtitulo.TLabel"
        ).grid(row=0, column=0, sticky="w", padx=(0, 15), pady=10)

        self.entrada_patente = ttk.Entry(
            formulario,
            textvariable=self.patente,
            width=25
        )
        self.entrada_patente.grid(row=0, column=1, pady=10)

        ttk.Label(
            formulario,
            text="Teléfono de contacto:",
            style="Subtitulo.TLabel"
        ).grid(row=1, column=0, sticky="w", padx=(0, 15), pady=10)

        ttk.Entry(
            formulario,
            textvariable=self.contacto,
            width=25
        ).grid(row=1, column=1, pady=10)

        botones = ttk.Frame(self, style="Contenedor.TFrame")
        botones.pack(anchor="w", padx=30, pady=20)

        ttk.Button(
            botones,
            text="Registrar",
            command=self._registrar,
            style="Accion.TButton"
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            botones,
            text="Limpiar",
            command=self._limpiar,
            style="Accion.TButton"
        ).pack(side="left")

    def _registrar(self):
        patente = self.patente.get().strip().upper()
        contacto = self.contacto.get().strip()

        if not patente or not contacto:
            messagebox.showerror(
                "Datos incompletos",
                "Debe completar todos los campos.",
                parent=self
            )
            return

        if len(patente) != 6 or not patente.isalnum():
            messagebox.showerror(
                "Patente inválida",
                "La patente debe tener 6 caracteres, solo letras y números.",
                parent=self
            )
            return

        if len(contacto) != 9 or not (
            contacto.isascii() and contacto.isdigit()
        ):
            messagebox.showerror(
                "Contacto inválido",
                "El teléfono debe contener exactamente 9 dígitos.",
                parent=self
            )
            return

        self.patente.set(patente)
        self.contacto.set(contacto)

        # El guardado se conectará con el servicio en otra etapa.
        messagebox.showinfo(
            "Validación correcta",
            "Los datos son válidos.\n"
            "El vehículo todavía no se ha guardado: "
            "falta conectar el servicio de registro.",
            parent=self
        )

    def _limpiar(self):
        self.patente.set("")
        self.contacto.set("")
        self.entrada_patente.focus_set()