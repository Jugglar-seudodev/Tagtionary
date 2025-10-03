import tkinter as tk
from tkinter import ttk
from funcionalidades.search_by_keyword import search_by_keyword  # type: ignore
from funcionalidades.crear_listados import crear_listados  # type: ignore
from system.ventana_nueva import crear_ventana_nueva  # Importar la función para la nueva ventana

def controlar_vista(ventana, vista, frame_cont, data):
    """
    Cambia la vista de la ventana principal según la opción seleccionada en el menú.
    
    :param ventana: La ventana principal de Tkinter.
    :param vista: Nombre de la vista que se seleccionó ("buscar" o "listados").
    :param frame_cont: El contenedor donde se cambiará la vista.
    :param data: Los datos cargados desde el archivo db.txt.
    """
    # Limpiar el contenedor actual
    for widget in frame_cont.winfo_children():
        widget.destroy()

    # Mostrar la vista seleccionada
    if vista == "buscar":
        search_by_keyword(frame_cont)
    elif vista == "listados":
        crear_listados(frame_cont)
    pass


def crear_menu(ventana, frame_cont, data):
    """
    Crea una barra de menús en la ventana principal y configura las opciones.
    
    :param ventana: La ventana principal de Tkinter.
    :param frame_cont: El contenedor donde se actualizará la vista.
    :param data: Los datos cargados desde el archivo db.txt.
    """
    menu_bar = tk.Menu(ventana)
    ventana.config(menu=menu_bar)

    # Crear el menú "Opciones"
    opciones_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Options", menu=opciones_menu)

    # Crear el menú "Opciones"
    op_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="New Window", menu=op_menu)

    # Opción para "Crear Listados"
    opciones_menu.add_command(label="Search by tag type", command=lambda: controlar_vista(ventana, "listados", frame_cont, data))
    
    # Opción para "Buscar por Palabra Clave"
    opciones_menu.add_command(label="Search by tag", command=lambda: controlar_vista(ventana, "buscar", frame_cont, data))

    # Opción para "Nueva Ventana"
    op_menu.add_command(label="Create", command=lambda: crear_ventana_nueva(ventana, data))
    
