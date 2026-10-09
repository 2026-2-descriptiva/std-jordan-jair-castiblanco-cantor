def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta: 

        [("A", 8), ("B", 7), ("C", 5), ...]
    """

 
    import gzip

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:

        conteo = {}

        for linea in archivo:
            letra = linea.split()[0]

            if letra in conteo:
                conteo[letra] += 1
            else:
                conteo[letra] = 1

        resultado = []

        for letra, cantidad in conteo.items():
            resultado.append((letra, cantidad))

        resultado.sort()

        return resultado
