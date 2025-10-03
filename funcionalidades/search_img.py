import os
import sys
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
    # Unir la base con la ruta proporcionada
    return os.path.normpath(os.path.join(base_path, ruta))

def search_img(tag_global, tag, sub_tag, dato, label_resultado, frame_cont):
    # Crear el texto de los resultados para mostrarlo en la interfaz
    resultado = f"Search result for: {tag_global}, {tag}, {sub_tag}, {dato}"  # Ejemplo de resultado
    label_resultado.config(text=resultado)    

    # Variables para almacenar los datos recopilados
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
                resultado += "\nData not found."
         
        # Si se encontró el valor en la columna 3 de descripciones.txt
        if valor_columna_3:
            ruta_imagenes = obtener_ruta_relativa('./data/imagenes.txt')
            with open(ruta_imagenes, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
                for line in lines:
                    columns = line.strip().split('\t')  # Usar tabulador como separador
                    if columns[0] == valor_columna_3:  # Si la primera columna coincide con el valor buscado
                        # Agregar las rutas absolutas de las imágenes
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
            
        # # Importación perezosa de crear_listados
        # from funcionalidades.crear_listados import crear_listados  # Importar aquí para evitar la circularidad
        # crear_listados(frame_cont)
    
    except FileNotFoundError as e:
        resultado += f"\nFile not found: {str(e)}"
    except UnicodeDecodeError:
        resultado += "\nEncoding error while reading files."
    except Exception as e:
        resultado += f"\nAn error occurred: {str(e)}"

    # # Actualizar el texto del Label con los resultados
    # label_resultado.config(text=resultado)
