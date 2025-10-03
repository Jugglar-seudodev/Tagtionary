import os
import sys
import tkinter as tk
from tkinter import ttk
from funcionalidades.cargar_datos import cargar_datos_desde_ultima_columna  # type: ignore
from system.ver_imagen import mostrar_imagenes  # Importar mostrar_imagenes

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
    return os.path.normpath(os.path.join(base_path, ruta))

# Variables globales para almacenar el estado
estado_busqueda = {
    "seleccionado": None,  # Valor actualmente seleccionado
    "sugerencias": []      # Sugerencias actuales en el Listbox
}

def search_by_keyword(frame_cont):
    # Cargar datos de la última columna
    data = cargar_datos_desde_ultima_columna()

    # Crear un contenedor para la búsqueda
    frame_busqueda = ttk.Frame(frame_cont)
    frame_busqueda.pack(pady=10, padx=10, fill="both", expand=True)

    # Etiqueta para la búsqueda
    ttk.Label(frame_busqueda, text="Search by tag name:").pack(pady=5)

    # Crear un Entry para la búsqueda
    entry_busqueda = ttk.Entry(frame_busqueda, width=40)
    entry_busqueda.pack(pady=5)

    # Crear un Frame para el Listbox y la Scrollbar
    listbox_frame = ttk.Frame(frame_busqueda)
    listbox_frame.pack(pady=5, padx=10)

    # Crear un Listbox para mostrar las sugerencias de búsqueda
    listbox_busqueda = tk.Listbox(listbox_frame, height=5, width=40, selectmode=tk.SINGLE)
    listbox_busqueda.pack(side="left", fill="both", expand=True)

    # Crear un Label para mostrar los resultados seleccionados
    label_resultado = ttk.Label(frame_busqueda, text="", justify="left", width=0)
    label_resultado.pack(pady=10)

    # Restaurar el estado previo
    if estado_busqueda["sugerencias"]:
        listbox_busqueda.delete(0, tk.END)
        for item in estado_busqueda["sugerencias"]:
            listbox_busqueda.insert(tk.END, item)

    # Función para actualizar las sugerencias en el Listbox
    def actualizar_completar(event):
        palabra = entry_busqueda.get().lower()  # Convertir a minúsculas para búsqueda insensible a mayúsculas

        # Filtrar los datos para mostrar solo aquellos que contengan la palabra escrita
        palabras_coincidentes = [dato for dato in data if palabra in dato.lower()]

        # Limitar a los primeros 10 elementos
        palabras_coincidentes = palabras_coincidentes[:10]

        # Limpiar el Listbox y agregar las palabras coincidentes
        listbox_busqueda.delete(0, tk.END)
        for item in palabras_coincidentes:
            listbox_busqueda.insert(tk.END, item)

        # Actualizar el estado global
        estado_busqueda["sugerencias"] = palabras_coincidentes

    # Función para mostrar el resultado seleccionado al hacer clic en una opción del Listbox
    def mostrar_resultado(event):
        seleccionado = listbox_busqueda.curselection()  # Obtener índice de la selección
        if seleccionado:  # Verificar si hay algo seleccionado
            valor_seleccionado = listbox_busqueda.get(seleccionado[0])
            label_resultado.config(text=f"Selected result: {valor_seleccionado}")
            buscar_imagenes(valor_seleccionado)  # Buscar usando el valor seleccionado

            # Actualizar el estado global
            estado_busqueda["seleccionado"] = valor_seleccionado
        else:
            label_resultado.config(text="No element selected.")

    # Función para buscar las imágenes relacionadas al valor seleccionado
    def buscar_imagenes(dato):
        resultado = f"Search result for: {dato}"
        datos_imagen = {}
        imagenes = []

        try:
            # Buscar en el archivo descripciones.txt
            valor_columna_3 = None
            ruta_descripciones = obtener_ruta_relativa('./data/descripciones.txt')
            with open(ruta_descripciones, 'r', encoding='utf-8') as file:
                lines = file.readlines()

                for line in lines:
                    columns = line.strip().split('\t')  # Usar tabulador como separador
                    if columns[0] == dato:  # Si la primera columna coincide con 'dato'
                        datos_imagen["nombre"] = columns[0]
                        datos_imagen["descripcion"] = (
                            f"POST 1: {columns[3]}\n"
                            f"POST 2: {columns[4]}\n\n"
                            f"{columns[1]}"
                        )
                        valor_columna_3 = columns[2]
                        resultado += f"\nColumna 1: {columns[0]}\nColumna 2: {columns[1]}\nColumna 3: {columns[2]}"
                        break
                else:
                    resultado += "\nNo se encontró el dato en descripciones.txt."

            # Si se encontró el valor en la columna 3 de descripciones.txt
            if valor_columna_3:
                ruta_imagenes = obtener_ruta_relativa('./data/imagenes.txt')
                with open(ruta_imagenes, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                    for line in lines:
                        columns = line.strip().split('\t')  # Usar tabulador como separador
                        if columns[0] == valor_columna_3:  # Si la primera columna coincide con el valor buscado
                            if columns[2] == 'no_imagen_02.png':
                                imagen_ruta = obtener_ruta_relativa("./imagenes/no_imagen/no_imagen_02.png")
                                imagenes.append(imagen_ruta)
                            else:
                                imagen_ruta = obtener_ruta_relativa(f"./imagenes/{columns[1]}/{columns[2]}")
                                imagenes.append(imagen_ruta)

                            if columns[4] == "no_imagen_02.png":                            
                                imagen_ruta_extra = obtener_ruta_relativa("./imagenes/no_imagen/no_imagen_02.png")
                                imagenes.append(imagen_ruta_extra)
                            else:    
                                imagen_ruta_extra = obtener_ruta_relativa(f"./imagenes/{columns[1]}/{columns[4]}")
                                imagenes.append(imagen_ruta_extra)

                            break
                    else:
                        resultado += "\nValue not found."

            # Llamar a mostrar_imagenes si se tienen datos válidos
            if datos_imagen and imagenes:
                mostrar_imagenes(frame_cont, datos_imagen, imagenes)
                search_by_keyword(frame_cont)

        except FileNotFoundError as e:
            resultado += f"\nValue not found. {str(e)}"
        except UnicodeDecodeError:
            resultado += "\nEncoding error while reading files."
        except Exception as e:
            resultado += f"\nAn error occurred: {str(e)}"

    # Asociar el evento de escritura en el Entry para actualizar las sugerencias
    entry_busqueda.bind("<KeyRelease>", actualizar_completar)

    # Asociar el evento de selección en el Listbox para mostrar el resultado seleccionado
    listbox_busqueda.bind("<ButtonRelease-1>", mostrar_resultado)

    # Permitir desplazamiento con la rueda del mouse
    def scroll_listbox(event):
        listbox_busqueda.yview_scroll(-1 * (event.delta // 120), "units")

    listbox_busqueda.bind("<MouseWheel>", scroll_listbox)
