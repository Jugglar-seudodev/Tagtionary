import tkinter as tk
from tkinter import Toplevel, Label, Canvas, Scrollbar
from PIL import Image, ImageTk

# Variable global para asegurarse de que solo se muestre una ventana a la vez
ventana_imagen = None

def mostrar_imagen_original(event, image_path):
    """
    Muestra la imagen en sus dimensiones originales al pasar el mouse sobre ella.
    La imagen se cerrará automáticamente después de 20 segundos.

    :param event: Evento de Tkinter (movimiento del mouse).
    :param image_path: Ruta de la imagen a mostrar.
    """
    global ventana_imagen

    # Verificar si ya hay una ventana abierta
    if ventana_imagen is not None:
        # Si ya está abierta, no hacer nada
        return

    # Crear una nueva ventana para mostrar la imagen
    ventana_imagen = Toplevel()
    ventana_imagen.title("Scale image 70% width and 60% height")

    # Abrir la imagen y escalarla a 3/4 de su tamaño original
    image = Image.open(image_path)
    original_width, original_height = image.size
    scaled_width = int(original_width * 0.7)
    scaled_height = int(original_height * 0.6)
    image = image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    # Mostrar la imagen en la ventana
    label_imagen = Label(ventana_imagen, image=photo)
    label_imagen.image = photo  # Mantener una referencia a la imagen
    label_imagen.pack()

    # Configurar la posición de la ventana cerca del mouse
    ventana_imagen.geometry(f"+{event.x_root + 0}+{event.y_root + 0}")

    # Cerrar la ventana después de 10 segundos
    ventana_imagen.after(10000, cerrar_ventana)

    # Cerrar la ventana cuando se mueva el mouse fuera
    ventana_imagen.bind("<Leave>", cerrar_ventana)

    # Cerrar la ventana manualmente y restablecer la variable global
    ventana_imagen.protocol("WM_DELETE_WINDOW", cerrar_ventana)

def cerrar_ventana():
    """
    Cierra la ventana emergente de la imagen original y restablece la variable global.
    """
    global ventana_imagen
    if ventana_imagen is not None:
        ventana_imagen.destroy()
        ventana_imagen = None  # Restablecer la variable global

def mostrar_imagen_derecho(event, image_path):
    """
    Muestra la imagen en su tamaño original en una nueva ventana al hacer clic con el botón derecho.

    :param event: Evento de Tkinter (clic derecho).
    :param image_path: Ruta de la imagen a mostrar.
    """
    global ventana_imagen

    # Verificar si ya hay una ventana abierta
    if ventana_imagen is not None:
        # Si ya está abierta, no hacer nada
        return

    # Crear una nueva ventana para mostrar la imagen
    ventana_imagen = Toplevel()
    ventana_imagen.title("Imagen Original")

    # Abrir la imagen en tamaño original
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    # Crear un lienzo para agregar la imagen y habilitar el desplazamiento
    canvas = Canvas(ventana_imagen, width=image.width, height=image.height)
    canvas.pack(side="left", expand=True)

    # Crear un Scrollbar vertical para el lienzo
    scrollbar = Scrollbar(ventana_imagen, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configurar el lienzo para usar el scrollbar
    canvas.config(yscrollcommand=scrollbar.set)

    # Agregar la imagen al lienzo
    canvas.create_image(0, 0, image=photo, anchor="nw")

    # Mantener la referencia de la imagen para evitar que sea recolectada por el garbage collector
    canvas.image = photo

    # Configurar el área del lienzo para que sea más grande que la ventana si la imagen lo requiere
    canvas.config(scrollregion=canvas.bbox("all"))

    # Hacer que la ventana ajuste su tamaño a la imagen
    ventana_imagen.update_idletasks()
    ventana_imagen.geometry(f"+{event.x_root}+{event.y_root}")

    # Asignar el evento para el desplazamiento con la rueda del mouse
    canvas.bind_all("<MouseWheel>", lambda e: desplazamiento_con_rueda(e, canvas))

    # Cerrar la ventana después de 10 segundos
    ventana_imagen.after(10000, cerrar_ventana)

    # Cerrar la ventana cuando se mueva el mouse fuera
    ventana_imagen.bind("<Leave>", cerrar_ventana)

    # Cerrar la ventana manualmente y restablecer la variable global
    ventana_imagen.protocol("WM_DELETE_WINDOW", cerrar_ventana)

def desplazamiento_con_rueda(event, canvas):
    """
    Permite el desplazamiento vertical de la imagen utilizando la rueda del mouse.

    :param event: Evento del mouse (movimiento de la rueda).
    :param canvas: El lienzo donde se muestra la imagen.
    """
    # Determinar la dirección del desplazamiento
    if event.delta < 0:
        canvas.yview_scroll(1, "units")  # Desplazar hacia abajo
    else:
        canvas.yview_scroll(-1, "units")  # Desplazar hacia arriba