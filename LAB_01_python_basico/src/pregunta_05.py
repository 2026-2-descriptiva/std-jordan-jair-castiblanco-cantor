def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    import gzip

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:
        valores_por_letra = {}

        for linea in archivo:
            letra, valor = linea.split()[0], int(linea.split()[1])

            if letra in valores_por_letra:
                valores_por_letra[letra].append(valor)
            else:
                valores_por_letra[letra] = [valor]

        resultado = []

        for letra, valores in valores_por_letra.items():
            maximo = max(valores)
            minimo = min(valores)
            resultado.append((letra, maximo, minimo))

        resultado.sort()

        return resultado
