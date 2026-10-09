def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta: 

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    import gzip

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:

        conteo = {}

        for linea in archivo:
            metrics = linea.split()[4]

            metricas = metrics.split(",")

            for metrica in metricas:
                clave, valor = metrica.split(":")

                if clave in conteo:
                    conteo[clave] += 1
                else:
                    conteo[clave] = 1

        resultado = {}

        for clave in sorted(conteo):
            resultado[clave] = conteo[clave]

        return resultado

