import tkinter as tk
from tkinter import Text
from tkinter import ttk
import re
from PIL import Image, ImageTk  # Para el manejo de imágenes
import os
from system.hover_image import mostrar_imagen_original, mostrar_imagen_derecho  # Importa la función desde el archivo system
from tkinter import Text, Scrollbar, Frame

def mostrar_imagenes(frame_cont, data, imagenes):
    """
    Función para mostrar el nombre, descripción y las imágenes en la interfaz.
    :param frame_cont: Contenedor principal donde se colocarán los widgets.
    :param data: Diccionario con la información, que incluye nombre, descripción e imágenes.
    :param imagenes: Lista de rutas de imágenes para mostrar en el lado derecho.
    """
    # Limpiar el contenedor de la vista anterior
    for widget in frame_cont.winfo_children():
        widget.destroy()

    # Obtener las dimensiones de la pantalla
    pantalla_ancho = frame_cont.winfo_screenwidth()
    pantalla_alto = frame_cont.winfo_screenheight()

    # Calcular el tamaño de la ventana como 3/4 de ancho y 1/3 de alto de la pantalla
    ancho_ventana = int(pantalla_ancho * 0.33)
    alto_ventana = int(pantalla_alto * 0.75)

    ancho = int((pantalla_ancho - ancho_ventana) / 2)
    alto = int((pantalla_alto - alto_ventana) / 2)

    # Crear un contenedor para la vista de la imagen
    frame_imagenes = ttk.Frame(frame_cont)
    frame_imagenes.pack(side="bottom", pady=50, padx=10, expand=True)
 
    # Nombre y descripción a la izquierda
    frame_izquierda = ttk.Frame(frame_imagenes, width=ancho, height=alto)
    frame_izquierda.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    
    # Crear un widget Text para mostrar el nombre y permitir la selección
    nombre_text = Text(frame_izquierda, height=1, width=27, wrap="none", font=("Arial", 12, "bold"))
    nombre_text.insert("1.0", data.get("nombre", "No disponible"))
    nombre_text.config(state="disabled")  # Hacerlo de solo lectura
    nombre_text.pack(anchor="w")

    # Crear un Frame para contener el widget Text y la barra de desplazamiento
    frame_texto = Frame(frame_izquierda)
    frame_texto.pack(pady=10)


    descripcion_label  = Text(
    #frame_izquierda,
    frame_texto, 
    wrap="word",  # Ajustar texto automáticamente
    height=15,  # Altura en líneas
    width=30,  # Ancho en caracteres
    )

    # Crear una barra de desplazamiento vertical
    scrollbar = Scrollbar(frame_texto, orient="vertical", command=descripcion_label.yview)
    descripcion_label.config(yscrollcommand=scrollbar.set)

    # Obtener la descripción con las etiquetas HTML
    descripcion_texto = data.get("descripcion", "No disponible")

    # Reemplazar las etiquetas <h4> y <h5> por saltos de línea (\n)
    descripcion_texto = descripcion_texto.replace("<h4>", "\n")
    descripcion_texto = descripcion_texto.replace("<h5>", "\n")

    # Insertar "Descripción:" una sola vez
    descripcion_label.insert("1.0", "")

    # Insertar el texto con los saltos de línea (que ahora reemplazan a <h4> y <h5>)
    descripcion_label.insert("end", descripcion_texto)

    # Configurar el widget de solo lectura
    descripcion_label.config(state="disabled")

    # Empacar el widget Text y la barra de desplazamiento
    descripcion_label.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")



    # Crear un frame para las imágenes a la derecha
    frame_derecha = ttk.Frame(frame_imagenes)
    frame_derecha.grid(row=0, column=1, padx=10, pady=10) # Reducir padx para moverlo más a la izquierda

    # Función para mostrar la imagen escalada
    def mostrar_imagen(imagen_index):
        image_path = imagenes[imagen_index]
        image = Image.open(image_path)
        screen_width = frame_cont.winfo_screenwidth()
        screen_height = frame_cont.winfo_screenheight()

        # Escalar la imagen a 1/3 del tamaño de la pantalla
        image = image.resize((int(screen_width // 8), int(screen_height // 3)))
        photo = ImageTk.PhotoImage(image)

        # Etiqueta para mostrar la imagen
        image_label.config(image=photo)
        image_label.image = photo  # Mantener una referencia a la imagen

        # Asociar el evento de hover con la función
        image_label.bind("<Button-1>", lambda event: mostrar_imagen_original(event, image_path))

         # Asociar el evento de hover con la función
        image_label.bind("<Button-3>", lambda event: mostrar_imagen_derecho(event, image_path))


    # Etiqueta para la imagen
    image_label = ttk.Label(frame_derecha)
    image_label.grid(row=0, column=0)

    # Botones para cambiar entre imágenes
    current_index = 0  # Índice actual de la imagen



    def cambiar_imagen(accion):
        nonlocal current_index
        if accion == "siguiente":
            current_index = (current_index + 1) % len(imagenes)
        elif accion == "anterior":
            current_index = (current_index - 1) % len(imagenes)
        mostrar_imagen(current_index)

    # Botones de navegación
    boton_anterior = ttk.Button(frame_derecha, text="Changing", command=lambda: cambiar_imagen("anterior"))
    boton_anterior.grid(row=1, column=0, padx=0, pady=5)  # Cambiar padx y agregar sticky

    # boton_siguiente = ttk.Button(frame_derecha, text="Siguiente", command=lambda: cambiar_imagen("siguiente"))
    # boton_siguiente.grid(row=1, column=1, padx=0, pady=5, sticky="w")  # Cambiar padx y agregar sticky

    # Mostrar la primera imagen por defecto
    mostrar_imagen(current_index)

    
