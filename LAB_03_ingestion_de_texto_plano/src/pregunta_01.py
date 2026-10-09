def pregunta_01():
    """ 
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

def pregunta_01():
    import pandas as pd

    registros = []
    hay_cluster = False
    palabras_clave = ""

    with open("data/clusters_report.txt", "r", encoding="utf-8") as archivo:

        for linea in archivo:
            elementos = linea.split()

            if elementos and elementos[0].isdigit():

                if hay_cluster:

                    texto = " ".join(palabras_clave.split())
                    palabras = texto.split(",")

                    palabras_limpias = []

                    for palabra in palabras:
                        palabra = palabra.strip()

                        if palabra:
                            palabras_limpias.append(palabra)

                    registro = {
                        "cluster": cluster,
                        "cantidad_de_palabras_clave": cantidad,
                        "porcentaje_de_palabras_clave": porcentaje,
                        "principales_palabras_clave": ", ".join(palabras_limpias).rstrip(".")
                    }

                    registros.append(registro)

                cluster = int(elementos[0])
                cantidad = int(elementos[1])
                porcentaje = float(elementos[2].replace(",", "."))

                partes = linea.split("%", 1)
                palabras_clave = partes[1].strip()

                hay_cluster = True

            else:
                if hay_cluster:
                    palabras = linea.strip()

                    if palabras:
                        palabras_clave += " " + palabras

        if hay_cluster:

            texto = " ".join(palabras_clave.split())
            palabras = texto.split(",")

            palabras_limpias = []

            for palabra in palabras:
                palabra = palabra.strip()

                if palabra:
                    palabras_limpias.append(palabra)

            registro = {
                "cluster": cluster,
                "cantidad_de_palabras_clave": cantidad,
                "porcentaje_de_palabras_clave": porcentaje,
                "principales_palabras_clave": ", ".join(palabras_limpias).rstrip(".")
            }

            registros.append(registro)

    return pd.DataFrame(registros)