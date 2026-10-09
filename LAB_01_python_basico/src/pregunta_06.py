def pregunta_06(): 
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """

    import gzip

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:

        valores_por_clave = {}

        for linea in archivo:
            metrics = linea.split()[4]

            metricas = metrics.split(",")

            for metrica in metricas:
                clave, valor = metrica.split(":")
                valor = int(valor)

                if clave in valores_por_clave:
                    valores_por_clave[clave].append(valor)
                else:
                    valores_por_clave[clave] = [valor]

        resultado = []

        for clave, valores in valores_por_clave.items():
            maximo = max(valores)
            minimo = min(valores)

            resultado.append((clave, minimo, maximo))

        resultado.sort()

        return resultado

