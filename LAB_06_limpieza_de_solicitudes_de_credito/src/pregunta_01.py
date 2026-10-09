def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """

import pandas as pd


def pregunta_01():

    solicitudes = pd.read_csv(
        "data/solicitudes_de_credito.csv.gz",
        sep=";"
    )

    # Eliminar columna de índice
    solicitudes = solicitudes.drop(columns=["Unnamed: 0"])


    # Eliminar registros incompletos,
    # excepto cuando falta comuna_ciudadano
    columnas_sin_comuna = solicitudes.columns.drop("comuna_ciudadano")

    solicitudes = solicitudes.dropna(subset=columnas_sin_comuna)



    # Normalizar campos de texto
    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito"
    ]

    for columna in columnas_texto:
        solicitudes[columna] = (
            solicitudes[columna]
            .str.strip()
            .str.lower()
            .str.replace("-", " ", regex=False)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )


    # Limpiar monto del crédito
    solicitudes["monto_del_credito"] = (
        solicitudes["monto_del_credito"]
        .str.strip()
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(".00", "", regex=False)
    )
    solicitudes["monto_del_credito"] = solicitudes["monto_del_credito"].astype(int)

    solicitudes["fecha_de_beneficio"] = (
    solicitudes["fecha_de_beneficio"]
    .str.strip()
    .str.replace("/", "-", regex=False))

    # Normalizar formato de fechas
    def convertir_fecha(fecha):
        partes = fecha.split("-")

        if len(partes[0]) == 4:
            return fecha

        dia, mes, año = partes

        return f"{año}-{mes.zfill(2)}-{dia.zfill(2)}"

    solicitudes["fecha_de_beneficio"] = (
        solicitudes["fecha_de_beneficio"].apply(convertir_fecha)
    )


    # Eliminar registros duplicados
    solicitudes = solicitudes.drop_duplicates()

    # Eliminar registros duplicados
    solicitudes = solicitudes.drop_duplicates()

    solicitudes.to_csv(
    "submission/solicitudes_de_credito.csv",
    sep=";",
    index=False)


pregunta_01()
