def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """


    import gzip

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:

        sumas = {}

        for linea in archivo:
            columnas = linea.split()

            value = int(columnas[1])
            codes = columnas[3]

            codigos = codes.split(",")

            for codigo in codigos:

                if codigo in sumas:
                    sumas[codigo] += value
                else:
                    sumas[codigo] = value

        resultado = {}

        for clave in sorted(sumas):
            resultado[clave] = sumas[clave]

        return resultado


