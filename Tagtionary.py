import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'system'))  # Usando la ruta relativa

from ver_imagen import mostrar_imagenes  # Importar la función
import tkinter as tk
from tkinter import ttk  # Asegúrate de importar ttk
from funcionalidades.cargar_datos import cargar_datos  # type: ignore
from system.control_view import crear_menu  # type: ignore
from system.ver_imagen import mostrar_imagenes  # Importar la función


# Función para obtener la ruta correcta de las imágenes
def obtener_ruta_imagen(imagen_path):
    # Verificar si el script está empaquetado con PyInstaller
    if getattr(sys, 'frozen', False):
        # Si está empaquetado con PyInstaller, usar la ruta temporal
        base_path = sys._MEIPASS
    else:
        # Si está en modo desarrollo, usar la ruta del script
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta completa a la imagen
    return os.path.join(base_path, imagen_path)


# Crear la ventana principal
ventana = tk.Tk()

# Obtener rutas relativas para los iconos
ruta_icono_chico = obtener_ruta_imagen("./imagenes/iconos/icon-16.png")
ruta_icono_grande = obtener_ruta_imagen("./imagenes/iconos/icon-32.png")

# Crear los iconos utilizando las rutas calculadas
icono_chico = tk.PhotoImage(file=ruta_icono_chico)
icono_grande = tk.PhotoImage(file=ruta_icono_grande)

# Configurar los iconos de la ventana
ventana.iconphoto(True, icono_grande, icono_chico)

# Obtener las dimensiones de la pantalla
pantalla_ancho = ventana.winfo_screenwidth()
pantalla_alto = ventana.winfo_screenheight()

# Calcular el tamaño de la ventana como 3/4 de ancho y 1/3 de alto de la pantalla
ancho_ventana = int(pantalla_ancho * 0.33)
alto_ventana = int(pantalla_alto * 0.75)

# Configurar el tamaño de la ventana
ventana.geometry(f"{ancho_ventana}x{alto_ventana}")

# Centrar la ventana en la pantalla
x_ventana = int((pantalla_ancho - ancho_ventana) / 2)
y_ventana = int((pantalla_alto - alto_ventana) / 2)
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")

# Configurar el título de la ventana
ventana.title("Tagtionary")

# Crear un contenedor para cambiar las vistas
frame_cont = ttk.Frame(ventana)  # Usando ttk.Frame correctamente
frame_cont.pack(side="top", fill="both", expand=True, padx=10, pady=10)

# Cargar los datos desde db.txt
data = cargar_datos()
 
# Crear la barra de menús
crear_menu(ventana, frame_cont, data)

# Lista de rutas de imágenes actualizadas
imagenes = [
    obtener_ruta_imagen("./imagenes/no_imagen/test_01.png"),
    obtener_ruta_imagen("./imagenes/no_imagen/test_02.png")
]

# Datos de la imagen
datos_imagen = {
    "nombre": "TEST",
    "descripcion": "This first screen shows an example of a search \n\nLeft click to display the image at 70% \nRight click to display the image at 100% \n\nImages are only taken as examples in the description shows the publication where they were taken from Danbooru",
}

# Llamar a la función para mostrar los datos (esto debe ir después de la creación de la ventana)
mostrar_imagenes(frame_cont, datos_imagen, imagenes)

# Mantener la ventana abierta
ventana.mainloop()
