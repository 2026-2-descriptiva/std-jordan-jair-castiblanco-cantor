def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    import gzip

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:

        letras_por_valor = {}

        for linea in archivo:
            letra = linea.split()[0]
            valor = int(linea.split()[1])

            if valor in letras_por_valor:
                if letra not in letras_por_valor[valor]:
                    letras_por_valor[valor].append(letra)
            else:
                letras_por_valor[valor] = [letra]

        resultado = []

        for valor, letras in letras_por_valor.items():
            letras.sort()
            resultado.append((valor, letras))

        resultado.sort()

        return resultado


