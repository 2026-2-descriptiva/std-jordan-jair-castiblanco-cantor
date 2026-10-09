def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    import gzip

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:

        sumas = {}

        for linea in archivo:
            columnas = linea.split()

            letra = columnas[0]
            metrics = columnas[4]

            metricas = metrics.split(",")

            for metrica in metricas:
                clave, valor = metrica.split(":")
                valor = int(valor)

                if letra in sumas:
                    sumas[letra] += valor
                else:
                    sumas[letra] = valor

        resultado = {}

        for clave in sorted(sumas):
            resultado[clave] = sumas[clave]

        return resultado

