def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """

    import gzip

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:

        letras_por_valor = {}

        for linea in archivo:
            letra = linea.split()[0]
            valor = int(linea.split()[1])

            if valor in letras_por_valor:
                letras_por_valor[valor].append(letra)
            else:
                letras_por_valor[valor] = [letra]

        resultado = []

        for valor, letras in letras_por_valor.items():
            resultado.append((valor, letras))

        resultado.sort()

        return resultado

