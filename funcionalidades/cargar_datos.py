import os
import sys

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

# Función para cargar los datos desde db.txt
def cargar_datos():
    data = {}
    ruta_db = obtener_ruta_relativa("data/db.txt")  # Ruta relativa para db.txt
    with open(ruta_db, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            tag_global, tag, sub_tag, dato = linea.strip().split("\t")
            if tag_global not in data:
                data[tag_global] = {}
            if tag not in data[tag_global]:
                data[tag_global][tag] = {}
            if sub_tag not in data[tag_global][tag]:
                data[tag_global][tag][sub_tag] = []
            data[tag_global][tag][sub_tag].append(dato)
    return data

# Función para cargar los datos desde la última columna de db.txt
def cargar_datos_desde_ultima_columna():
    datos = []
    ruta_db = obtener_ruta_relativa("data/db.txt")  # Ruta relativa para db.txt
    with open(ruta_db, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")
            if len(columnas) > 0:  # Asegurarse de que la línea no esté vacía
                datos.append(columnas[-1])  # Agregar la última columna
    return datos
