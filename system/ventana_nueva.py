import tkinter as tk
from tkinter import ttk
from funcionalidades.search_by_keyword import search_by_keyword  # type: ignore
from funcionalidades.crear_listados import crear_listados  # type: ignore

def crear_ventana_nueva(ventana_principal, data):
    """
    Crea una nueva ventana a la derecha de la ventana principal con las mismas opciones,
    pero sin la posibilidad de abrir otra nueva ventana.
    
    :param ventana_principal: La ventana principal de Tkinter.
    :param data: Los datos cargados desde el archivo db.txt.
    """
    # Obtener tamaño y posición de la ventana principal
    ventana_principal.update_idletasks()  # Asegura que las dimensiones sean correctas
    ancho_principal = ventana_principal.winfo_width()
    alto_principal = ventana_principal.winfo_height()
    x_principal = ventana_principal.winfo_x()
    y_principal = ventana_principal.winfo_y()

    # Calcular posición de la nueva ventana (a la derecha de la principal)
    x_offset = x_principal + ancho_principal + 10
    y_offset = y_principal

    # Crear la nueva ventana
    nueva_ventana = tk.Toplevel(ventana_principal)
    nueva_ventana.title("Tagtionary-2")
    nueva_ventana.geometry(f"{ancho_principal}x{alto_principal}+{x_offset}+{y_offset}")  # Igual tamaño y posición calculada

    # Crear un contenedor para las vistas
    frame_cont = ttk.Frame(nueva_ventana)
    frame_cont.pack(fill="both", expand=True)

    # Crear una barra de menús para la nueva ventana
    menu_bar = tk.Menu(nueva_ventana)
    nueva_ventana.config(menu=menu_bar)

    # Crear el menú "Opciones"
    opciones_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Options", menu=opciones_menu)
    

    # Importar controlar_vista localmente
    from system.control_view import controlar_vista

    # Opción para "Crear Listados"
    opciones_menu.add_command(label="Search by tag type", command=lambda: controlar_vista(nueva_ventana, "listados", frame_cont, data))

    # Opción para "Buscar por Palabra Clave"
    opciones_menu.add_command(label="Search by tag", command=lambda: controlar_vista(nueva_ventana, "buscar", frame_cont, data))
