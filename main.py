
import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
from datetime import datetime
import webbrowser
import html

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

APP_NAME = "FormuDesk"

BASE_DIR = Path(__file__).resolve().parent
GENERATED_DIR = BASE_DIR / "generated"

GENERATED_DIR.mkdir(exist_ok=True)


# ==========================================
# CLASE PRINCIPAL
# ==========================================

class FormuDeskApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("750x650")
        self.minsize(650, 550)

        self.crear_interfaz()

    # ======================================
    # INTERFAZ GRÁFICA
    # ======================================

    def crear_interfaz(self):

        # Encabezado
        titulo = ctk.CTkLabel(
            self,
            text="FormuDesk",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=(25, 5))

        subtitulo = ctk.CTkLabel(
            self,
            text="Sistema de generación de documentos",
            font=("Arial", 14)
        )
        subtitulo.pack(pady=(0, 20))

        # Contenedor del formulario
        self.formulario = ctk.CTkFrame(self)
        self.formulario.pack(
            padx=40,
            pady=10,
            fill="both",
            expand=True
        )

        # Nombre
        ctk.CTkLabel(
            self.formulario,
            text="Nombre completo:"
        ).pack(anchor="w", padx=25, pady=(20, 5))

        self.nombre = ctk.CTkEntry(
            self.formulario,
            placeholder_text="Ingrese el nombre completo",
            height=38
        )
        self.nombre.pack(fill="x", padx=25)

        # Identificación
        ctk.CTkLabel(
            self.formulario,
            text="Número de identificación:"
        ).pack(anchor="w", padx=25, pady=(15, 5))

        self.identificacion = ctk.CTkEntry(
            self.formulario,
            placeholder_text="Ingrese la identificación",
            height=38
        )
        self.identificacion.pack(fill="x", padx=25)

        # Fecha
        ctk.CTkLabel(
            self.formulario,
            text="Fecha:"
        ).pack(anchor="w", padx=25, pady=(15, 5))

        self.fecha = ctk.CTkEntry(
            self.formulario,
            height=38
        )
        self.fecha.pack(fill="x", padx=25)

        self.fecha.insert(
            0,
            datetime.now().strftime("%d/%m/%Y")
        )

        # Descripción
        ctk.CTkLabel(
            self.formulario,
            text="Descripción:"
        ).pack(anchor="w", padx=25, pady=(15, 5))

        self.descripcion = ctk.CTkTextbox(
            self.formulario,
            height=100
        )
        self.descripcion.pack(fill="x", padx=25)

        # Botones
        contenedor_botones = ctk.CTkFrame(
            self.formulario,
            fg_color="transparent"
        )
        contenedor_botones.pack(pady=25)

        self.btn_generar = ctk.CTkButton(
            contenedor_botones,
            text="Generar documento",
            width=180,
            height=40,
            command=self.generar_documento
        )
        self.btn_generar.pack(side="left", padx=10)

        self.btn_limpiar = ctk.CTkButton(
            contenedor_botones,
            text="Limpiar formulario",
            width=180,
            height=40,
            fg_color="gray",
            hover_color="#555555",
            command=self.limpiar_formulario
        )
        self.btn_limpiar.pack(side="left", padx=10)

    # ======================================
    # OBTENER Y VALIDAR INFORMACIÓN
    # ======================================

    def obtener_datos(self):

        datos = {
            "nombre": self.nombre.get().strip(),
            "identificacion": self.identificacion.get().strip(),
            "fecha": self.fecha.get().strip(),
            "descripcion": self.descripcion.get("1.0", "end-1c").strip()
        }

        if not datos["nombre"]:
            messagebox.showwarning(
                "Campo obligatorio",
                "Debe ingresar el nombre completo."
            )
            self.nombre.focus()
            return None

        if not datos["identificacion"]:
            messagebox.showwarning(
                "Campo obligatorio",
                "Debe ingresar la identificación."
            )
            self.identificacion.focus()
            return None

        if not datos["fecha"]:
            messagebox.showwarning(
                "Campo obligatorio",
                "Debe ingresar la fecha."
            )
            self.fecha.focus()
            return None

        return datos

    # ======================================
    # GENERAR DOCUMENTO HTML
    # ======================================

    def generar_documento(self):

        datos = self.obtener_datos()

        if datos is None:
            return

        # Escapar caracteres especiales para HTML
        nombre = html.escape(datos["nombre"])
        identificacion = html.escape(datos["identificacion"])
        fecha = html.escape(datos["fecha"])
        descripcion = html.escape(datos["descripcion"])

        plantilla = (BASE_DIR / "templates" / "plantilla.html").read_text(
            encoding="utf-8"
        )
        contenido_html = (
            plantilla
            .replace("{{NOMBRE}}", nombre)
            .replace("{{IDENTIFICACION}}", identificacion)
            .replace("{{FECHA}}", fecha)
            .replace("{{DESCRIPCION}}", descripcion)
        )

        # Crear archivo HTML
        nombre_archivo = (
            f"documento_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.html"
        )

        ruta_archivo = GENERATED_DIR / nombre_archivo

        ruta_archivo.write_text(
            contenido_html,
            encoding="utf-8"
        )

        # Abrir documento en el navegador
        webbrowser.open(ruta_archivo.resolve().as_uri())

        messagebox.showinfo(
            "Documento generado",
            "El documento se generó correctamente.\n"
            "Puedes revisarlo e imprimirlo desde el navegador."
        )

    # ======================================
    # LIMPIAR FORMULARIO
    # ======================================

    def limpiar_formulario(self):

        self.nombre.delete(0, "end")
        self.identificacion.delete(0, "end")

        self.fecha.delete(0, "end")
        self.fecha.insert(
            0,
            datetime.now().strftime("%d/%m/%Y")
        )

        self.descripcion.delete("1.0", "end")


# ==========================================
# EJECUCIÓN DEL PROGRAMA
# ==========================================

if __name__ == "__main__":

    app = FormuDeskApp()
    app.mainloop()
