def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """

    import gzip

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:
        suma_por_letra = {}

        for linea in archivo:
            letra, valor = linea.split()[0], int(linea.split()[1])

            if letra in suma_por_letra:
                suma_por_letra[letra] += valor
            else:
                suma_por_letra[letra] = valor

        resultado = []

        for letra, suma in suma_por_letra.items():
            resultado.append((letra, suma))

        resultado.sort()

        return resultado

print(pregunta_03())