def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """

    import gzip

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:

        resultado = []

        for linea in archivo:
            columnas = linea.split()

            letra = columnas[0]
            codes = columnas[3]
            metrics = columnas[4]

            codigos = codes.split(",")
            metricas = metrics.split(",")

            resultado.append((letra, len(codigos), len(metricas)))

        return resultado
