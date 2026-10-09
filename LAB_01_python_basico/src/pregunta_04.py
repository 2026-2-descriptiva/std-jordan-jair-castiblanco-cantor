def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.
 
    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """

    import gzip

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:

        conteo_por_mes = {}

        for linea in archivo:
            fecha = linea.split()[2]
            mes = fecha.split("-")[1]

            if mes in conteo_por_mes:
                conteo_por_mes[mes] += 1
            else:
                conteo_por_mes[mes] = 1

        resultado = []

        for mes, cantidad in conteo_por_mes.items():
            resultado.append((mes, cantidad))

        resultado.sort()

        return resultado
