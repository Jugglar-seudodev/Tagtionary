import tkinter as tk
from tkinter import ttk
from funcionalidades.cargar_datos import cargar_datos  # type: ignore # Importar cargar_datos
from funcionalidades.search_img import search_img  # type: ignore  # Importar search_img
import os
import sys

# Diccionario global para almacenar las selecciones actuales
selecciones_actuales = {
    "tag_global": "",
    "tag": "",
    "sub_tag": "",
    "dato": ""
}

# Clase para manejar el Tooltip
class Tooltip:
    def __init__(self, widget, text=""):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

    def show_tooltip(self, event):
        if not self.text:
            return
        x = event.x_root + 10
        y = event.y_root + 10
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.geometry(f"+{x}+{y}")
        label = ttk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack(ipadx=5, ipady=2)

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def agregar_tooltip_combobox(combobox):
    tooltip = Tooltip(combobox)
    def actualizar_tooltip(event):
        valor = combobox.get()
        if valor:
            tooltip.text = valor
            tooltip.show_tooltip(event)
    combobox.bind("<Enter>", actualizar_tooltip)
    combobox.bind("<Leave>", tooltip.hide_tooltip)

def actualizar_seleccion(event, combobox, clave):
    selecciones_actuales[clave] = combobox.get()

def restaurar_selecciones(combobox_tag_global, combobox_tag, combobox_sub_tag, combobox_dato, data):
    """
    Restaura las selecciones en los Combobox a partir del diccionario global
    y actualiza los dependientes.
    """
    # Restaurar tag_global y actualizar tags dependientes
    if selecciones_actuales["tag_global"]:
        combobox_tag_global.set(selecciones_actuales["tag_global"])
        actualizar_tags(
            None,  # Evento no necesario
            combobox_tag_global,
            combobox_tag,
            combobox_sub_tag,
            combobox_dato,
            data
        )

    # Restaurar tag y actualizar subtags dependientes
    if selecciones_actuales["tag"]:
        combobox_tag.set(selecciones_actuales["tag"])
        actualizar_subtags(
            None,  # Evento no necesario
            combobox_tag,
            combobox_sub_tag,
            combobox_dato,
            data,
            selecciones_actuales["tag_global"]
        )

    # Restaurar sub_tag y actualizar datos dependientes
    if selecciones_actuales["sub_tag"]:
        combobox_sub_tag.set(selecciones_actuales["sub_tag"])
        actualizar_datos(
            None,  # Evento no necesario
            combobox_sub_tag,
            combobox_dato,
            data,
            selecciones_actuales["tag_global"],
            selecciones_actuales["tag"]
        )

    # Restaurar dato
    if selecciones_actuales["dato"]:
        combobox_dato.set(selecciones_actuales["dato"])


# Interfaz de prueba
def crear_interfaz_prueba(root):
    # Crear un frame principal
    frame = ttk.Frame(root)
    frame.pack(padx=20, pady=20)

    # Combobox con valores largos
    combobox = ttk.Combobox(frame, values=["Corto", "Texto muy largo que requiere Tooltip", "Otro dato largo"], state="readonly")
    combobox.pack(pady=10)
    agregar_tooltip_combobox(combobox)


# Crear ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tooltip en Combobox")
    root.geometry("400x200")

    crear_interfaz_prueba(root)

    root.mainloop()

# Modificar la función `crear_listados` para incluir los Tooltips


def crear_listados(frame_cont):
    contenedor = ttk.Frame(frame_cont)
    contenedor.pack(side="top", pady=10, padx=10)
    contenedor.grid_columnconfigure(0, weight=1)
    contenedor.grid_columnconfigure(1, weight=1)
    contenedor.grid_columnconfigure(2, weight=1)
    contenedor.grid_columnconfigure(3, weight=1)

    data = cargar_datos()
    ttk.Label(contenedor, text="Select Data", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")
    ttk.Label(contenedor, text="Global Tag").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    ttk.Label(contenedor, text="Subcategory 1").grid(row=1, column=1, padx=10, pady=5, sticky="w")
    ttk.Label(contenedor, text="Subcategory 2").grid(row=1, column=2, padx=10, pady=5, sticky="w")
    ttk.Label(contenedor, text="Tag").grid(row=1, column=3, padx=10, pady=5, sticky="w")

    combobox_tag_global = ttk.Combobox(contenedor, state="readonly", width=20)
    combobox_tag_global.grid(row=2, column=0, padx=10, pady=5)
    combobox_tag_global['values'] = list(data.keys())
    agregar_tooltip_combobox(combobox_tag_global)

    combobox_tag = ttk.Combobox(contenedor, state="readonly", width=20)
    combobox_tag.grid(row=2, column=1, padx=10, pady=5)
    agregar_tooltip_combobox(combobox_tag)

    combobox_sub_tag = ttk.Combobox(contenedor, state="readonly", width=20)
    combobox_sub_tag.grid(row=2, column=2, padx=10, pady=5)
    agregar_tooltip_combobox(combobox_sub_tag)

    combobox_dato = ttk.Combobox(contenedor, state="readonly", width=20)
    combobox_dato.grid(row=2, column=3, padx=10, pady=5)
    agregar_tooltip_combobox(combobox_dato)

    label_resultado = ttk.Label(frame_cont, justify="left", width=50)
    label_resultado.pack(pady=10)

    def verificar_y_ejecutar(*args):
        tag_global_seleccionado = combobox_tag_global.get()
        tag_seleccionado = combobox_tag.get()
        sub_tag_seleccionado = combobox_sub_tag.get()
        dato_seleccionado = combobox_dato.get()

        if all([tag_global_seleccionado, tag_seleccionado, sub_tag_seleccionado, dato_seleccionado]):            
            search_img(tag_global_seleccionado, tag_seleccionado, sub_tag_seleccionado, dato_seleccionado, label_resultado, frame_cont)
            crear_listados(frame_cont)

    combobox_tag_global.bind("<<ComboboxSelected>>", lambda event: [
        actualizar_tags(event, combobox_tag_global, combobox_tag, combobox_sub_tag, combobox_dato, data),
        actualizar_seleccion(event, combobox_tag_global, "tag_global"),
        verificar_y_ejecutar()
    ])
    combobox_tag.bind("<<ComboboxSelected>>", lambda event: [
        actualizar_subtags(event, combobox_tag, combobox_sub_tag, combobox_dato, data, combobox_tag_global.get()),
        actualizar_seleccion(event, combobox_tag, "tag"),
        verificar_y_ejecutar()
    ])
    combobox_sub_tag.bind("<<ComboboxSelected>>", lambda event: [
        actualizar_datos(event, combobox_sub_tag, combobox_dato, data, combobox_tag_global.get(), combobox_tag.get()),
        actualizar_seleccion(event, combobox_sub_tag, "sub_tag"),
        verificar_y_ejecutar()
    ])
    combobox_dato.bind("<<ComboboxSelected>>", lambda event: [
        actualizar_seleccion(event, combobox_dato, "dato"),
        verificar_y_ejecutar()
    ])

    restaurar_selecciones(combobox_tag_global, combobox_tag, combobox_sub_tag, combobox_dato, data)

def obtener_ruta_relativa(ruta):
    """
    Obtiene la ruta relativa desde la raíz del proyecto.

    :param ruta: Ruta relativa desde la raíz del proyecto.
    :return: Ruta absoluta válida.
    """
    if getattr(sys, 'frozen', False):
        # Si está empaquetado con PyInstaller
        base_path = sys._MEIPASS
    else:
        # En desarrollo, se asume que el script principal está en la raíz del proyecto
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    # Unir la base con la ruta proporcionada
    return os.path.normpath(os.path.join(base_path, ruta))

def cargar_datos():
    """
    Carga los datos desde el archivo `db.txt` en la carpeta `data`.

    :return: Diccionario con los datos organizados.
    """
    data = {}
    ruta_archivo = obtener_ruta_relativa("./data/db.txt")  # Ruta adaptada

    # Leer el archivo db.txt en la carpeta data
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            # Separar los valores por tabulador
            tag_global, tag, sub_tag, dato = linea.strip().split("\t")

            # Organizar los datos en un diccionario por tag_global
            if tag_global not in data:
                data[tag_global] = {}

            if tag not in data[tag_global]:
                data[tag_global][tag] = {}

            if sub_tag not in data[tag_global][tag]:
                data[tag_global][tag][sub_tag] = []

            data[tag_global][tag][sub_tag].append(dato)

    return data

def actualizar_tags(event, combobox_tag_global, combobox_tag, combobox_sub_tag, combobox_dato, data):
    # Obtener el tag_global seleccionado
    tag_global_seleccionado = combobox_tag_global.get()

    # Limpiar y actualizar los tags dependientes
    combobox_tag.set("")
    combobox_tag['values'] = list(data[tag_global_seleccionado].keys())
    combobox_sub_tag.set("")
    combobox_sub_tag['values'] = []
    combobox_dato.set("")
    combobox_dato['values'] = []

def actualizar_subtags(event, combobox_tag, combobox_sub_tag, combobox_dato, data, tag_global_seleccionado):
    # Obtener el tag seleccionado
    tag_seleccionado = combobox_tag.get()

    # Limpiar y actualizar los sub-tags dependientes
    combobox_sub_tag.set("")
    combobox_sub_tag['values'] = list(data[tag_global_seleccionado][tag_seleccionado].keys())
    combobox_dato.set("")
    combobox_dato['values'] = []

def actualizar_datos(event, combobox_sub_tag, combobox_dato, data, tag_global_seleccionado, tag_seleccionado):
    # Obtener el sub-tag seleccionado
    sub_tag_seleccionado = combobox_sub_tag.get()

    # Limpiar y actualizar los datos dependientes
    combobox_dato.set("")
    combobox_dato['values'] = data[tag_global_seleccionado][tag_seleccionado][sub_tag_seleccionado]


