
import customtkinter as ctk
from tkinter import TclError, messagebox
from pathlib import Path
from datetime import datetime
import webbrowser
import hashlib
import html
import re
import sys
import os
import json
import subprocess
import tempfile
import threading
import urllib.request

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

APP_NAME = "FormuDesk"
VERSION = "1.0.0"
GITHUB_USER = "EdwinFigueroa2003"
GITHUB_REPO = "FormuDesk"
GITHUB_API = (
    f"https://api.github.com/repos/"
    f"{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
)

APP_DIR = (
    Path(sys.executable).resolve().parent
    if getattr(sys, "frozen", False)
    else Path(__file__).resolve().parent
)
RESOURCE_DIR = Path(
    getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
)
GENERATED_DIR = APP_DIR / "generated"

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

        self.after(
            1500,
            lambda: verificar_actualizaciones(self)
        )

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

        plantilla = (RESOURCE_DIR / "templates" / "plantilla.html").read_text(
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
# CONFIGURACIÓN DE ACTUALIZACIONES
# ==========================================

def version_tuple(version):
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", version.strip())
    if not match:
        raise ValueError(
            f"Versión no válida: {version}. Usa el formato v1.2.3."
        )
    return tuple(int(part) for part in match.groups())


def consultar_ultima_version():
    request = urllib.request.Request(
        GITHUB_API,
        headers={
            "User-Agent": APP_NAME,
            "Accept": "application/vnd.github+json"
        }
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        release = json.loads(response.read().decode("utf-8"))

    nueva_version = release.get("tag_name")
    if not isinstance(nueva_version, str) or not nueva_version:
        raise ValueError("GitHub no proporcionó la versión del release.")

    if version_tuple(nueva_version) <= version_tuple(VERSION):
        return None

    asset = next(
        (
            item for item in release.get("assets", [])
            if item.get("name") == "FormuDesk.exe"
        ),
        None
    )
    if asset is None:
        raise ValueError(
            "No se encontró FormuDesk.exe en los archivos del release."
        )

    return nueva_version, asset


def descargar_actualizacion(asset):
    download_url = asset.get("browser_download_url")
    if not isinstance(download_url, str) or not download_url.startswith("https://"):
        raise ValueError("GitHub no proporcionó una URL HTTPS válida.")

    digest = asset.get("digest", "")
    match = re.fullmatch(r"sha256:([0-9a-fA-F]{64})", digest)
    if not match:
        raise ValueError(
            "El release no contiene un SHA-256 válido para verificar."
        )

    descriptor, nombre_temporal = tempfile.mkstemp(
        prefix="FormuDesk_update_",
        suffix=".exe"
    )
    os.close(descriptor)
    ruta_temporal = Path(nombre_temporal)

    try:
        request = urllib.request.Request(
            download_url,
            headers={"User-Agent": APP_NAME}
        )
        sha256 = hashlib.sha256()

        with urllib.request.urlopen(request, timeout=120) as response:
            with ruta_temporal.open("wb") as archivo:
                while True:
                    bloque = response.read(1024 * 1024)
                    if not bloque:
                        break
                    archivo.write(bloque)
                    sha256.update(bloque)

        if sha256.hexdigest().lower() != match.group(1).lower():
            raise ValueError("La verificación SHA-256 de la descarga falló.")

        return ruta_temporal
    except Exception:
        try:
            ruta_temporal.unlink()
        except OSError:
            pass
        raise


def powershell_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def iniciar_reemplazo(app, actualizacion):
    if not getattr(sys, "frozen", False):
        raise RuntimeError(
            "La actualización automática solo funciona en la versión EXE."
        )

    ruta_app = Path(sys.executable).resolve()
    pid = os.getpid()
    ruta_script = Path(tempfile.gettempdir()) / (
        f"FormuDesk_update_{pid}.ps1"
    )

    script = f"""
$ErrorActionPreference = 'Stop'
$targetProcessId = {pid}
$target = {powershell_quote(ruta_app)}
$newFile = {powershell_quote(actualizacion)}
$staged = $target + '.new'
$backup = $target + '.bak'
$scriptPath = $MyInvocation.MyCommand.Path

try {{
    Wait-Process -Id $targetProcessId -ErrorAction SilentlyContinue
    Copy-Item -LiteralPath $newFile -Destination $staged -Force

    if (Test-Path -LiteralPath $backup) {{
        Remove-Item -LiteralPath $backup -Force
    }}

    Move-Item -LiteralPath $target -Destination $backup -Force

    try {{
        Move-Item -LiteralPath $staged -Destination $target -Force
        Start-Process -FilePath $target
    }}
    catch {{
        if (Test-Path -LiteralPath $target) {{
            Remove-Item -LiteralPath $target -Force
        }}
        if (Test-Path -LiteralPath $backup) {{
            Move-Item -LiteralPath $backup -Destination $target -Force
        }}
        throw
    }}

    Remove-Item -LiteralPath $backup -Force -ErrorAction SilentlyContinue
}}
catch {{
    Add-Type -AssemblyName PresentationFramework
    [System.Windows.MessageBox]::Show(
        "No se pudo instalar la actualización: $($_.Exception.Message)",
        "FormuDesk - Error"
    )
}}
finally {{
    Remove-Item -LiteralPath $newFile -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $staged -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $scriptPath -Force -ErrorAction SilentlyContinue
}}
"""

    try:
        ruta_script.write_text(script, encoding="utf-8-sig")
        subprocess.Popen(
            [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-File", str(ruta_script)
            ],
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )
    except Exception:
        if ruta_script.exists():
            ruta_script.unlink()
        if actualizacion.exists():
            actualizacion.unlink()
        raise

    app.destroy()


def programar_en_interfaz(app, callback):
    try:
        app.after(0, callback)
    except (RuntimeError, TclError):
        return False
    return True


def mostrar_error_actualizacion(app, error):
    if app.winfo_exists():
        messagebox.showwarning(
            "Actualización",
            f"No fue posible actualizar FormuDesk.\n\nDetalle: {error}",
            parent=app
        )


def confirmar_actualizacion(app, nueva_version, asset):
    if not app.winfo_exists():
        return

    respuesta = messagebox.askyesno(
        "Actualización disponible",
        f"Hay una nueva versión de FormuDesk: {nueva_version}\n\n"
        f"Versión instalada: {VERSION}\n\n"
        "¿Deseas descargarla e instalarla?",
        parent=app
    )
    if not respuesta:
        return

    threading.Thread(
        target=descargar_e_instalar,
        args=(app, asset),
        daemon=True
    ).start()


def descargar_e_instalar(app, asset):
    actualizacion = None
    try:
        actualizacion = descargar_actualizacion(asset)
        if not programar_en_interfaz(
            app,
            lambda: iniciar_actualizacion_desde_interfaz(app, actualizacion)
        ):
            actualizacion.unlink()
    except Exception as error:
        if actualizacion is not None and actualizacion.exists():
            try:
                actualizacion.unlink()
            except OSError:
                pass
        programar_en_interfaz(
            app,
            lambda error=error: mostrar_error_actualizacion(app, error)
        )


def iniciar_actualizacion_desde_interfaz(app, actualizacion):
    try:
        iniciar_reemplazo(app, actualizacion)
    except Exception as error:
        mostrar_error_actualizacion(app, error)


def verificar_actualizaciones(app):
    if not getattr(sys, "frozen", False):
        return

    def consultar_en_segundo_plano():
        try:
            resultado = consultar_ultima_version()
            if resultado is None:
                return

            nueva_version, asset = resultado
            programar_en_interfaz(
                app,
                lambda: confirmar_actualizacion(app, nueva_version, asset)
            )
        except Exception as error:
            programar_en_interfaz(
                app,
                lambda error=error: mostrar_error_actualizacion(app, error)
            )

    threading.Thread(
        target=consultar_en_segundo_plano,
        daemon=True
    ).start()

# ==========================================
# EJECUCIÓN DEL PROGRAMA
# ==========================================

if __name__ == "__main__":

    app = FormuDeskApp()
    app.mainloop()
