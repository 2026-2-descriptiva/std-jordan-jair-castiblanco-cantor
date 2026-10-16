import pandas as pd
import numpy as np


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """

    # Cargar los datos de cada canal
    web = pd.read_csv("data/historical_requests_web.csv.gz")
    letter = pd.read_csv("data/historical_requests_letter.csv.gz")

    # Eliminar filas completamente idénticas dentro de cada canal
    web = web.drop_duplicates()
    letter = letter.drop_duplicates()

    web["in_date"] = pd.to_datetime(web["in_date"])
    web["out_date"] = pd.to_datetime(web["out_date"])

    letter["in_date"] = pd.to_datetime(letter["in_date"])
    letter["out_date"] = pd.to_datetime(letter["out_date"])

    # creamos los canales de las pqrs
    web["channel"] = "web"
    letter["channel"] = "letter"

    union = pd.concat([web, letter], ignore_index=True)

    union["dia_calen"] = (union["out_date"] - union["in_date"]).dt.days

    # Identificar las solicitudes respondidas
    respondidas = union["out_date"].notna()

    # Convertir las fechas a precisión de días para NumPy
    fecha_entrada = union["in_date"].values.astype("datetime64[D]")
    fecha_respuesta = union["out_date"].values.astype("datetime64[D]")

    # Crear la columna de días hábiles
    union["dia_habil"] = np.nan

    union.loc[respondidas, "dia_habil"] = np.busday_count(
        fecha_entrada[respondidas.to_numpy()] + np.timedelta64(1, "D"),
        fecha_respuesta[respondidas.to_numpy()] + np.timedelta64(1, "D")
    )

    union["on_time"] = (
        union["dia_habil"].le(15)
        & union["out_date"].notna()
    )

    requests = union.groupby("channel").size()

    answered = (
    union.groupby("channel")["out_date"]
    .apply(lambda x: x.notna().sum())
    )

    pending = (
        union.groupby("channel")["out_date"]
        .apply(lambda x: x.isna().sum())
    )

    median_business_days = (
        union.groupby("channel")["dia_habil"]
        .median()
    )

    on_time_rate = (
    union.groupby("channel")["on_time"]
    .mean()
    )

    channel_summary = pd.DataFrame({
    "channel": requests.index,
    "requests": requests,
    "answered": answered,
    "pending": pending,
    "median_business_days": median_business_days,
    "on_time_rate": on_time_rate
    })

    channel_summary = channel_summary.reset_index(drop=True)
    
    channel_summary.to_csv(
        "submission/channel_summary.csv",
        index=False
    )

    union["year"] = union["in_date"].dt.year

    yearly_requests = (
        union.groupby(["year", "channel"])
        .size()
    )

    yearly_pending = (
    union.groupby(["year", "channel"])["out_date"]
    .apply(lambda x: x.isna().sum())
    )

    yearly_on_time_rate = (
    union.groupby(["year", "channel"])["on_time"]
    .mean()
    )

    # Construir la tabla resumen por año y canal
    yearly_summary = yearly_requests.rename("requests").to_frame()

    yearly_summary["pending"] = yearly_pending
    yearly_summary["on_time_rate"] = yearly_on_time_rate

    yearly_summary = yearly_summary.reset_index()

    # Organizar las columnas
    yearly_summary = yearly_summary[
        ["year", "channel", "requests", "pending", "on_time_rate"]
    ]

    # Ordenar por año y canal
    yearly_summary = yearly_summary.sort_values(
        ["year", "channel"]
    ).reset_index(drop=True)

    yearly_summary.to_csv(
        "submission/yearly_summary.csv",
        index=False
    )

    # Orden de los días de la semana
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    # Indicador 1: cantidad de solicitudes por día de entrada
    entry_day_requests = (
        union.groupby("day_name").size()
        .reindex(day_order, fill_value=0)
    )

    # Indicador 2: mediana de días calendario por día de entrada
    entry_day_calendar = (
        union.groupby("day_name")["dia_calen"]
        .median()
        .reindex(day_order)
    )

    # Indicador 3: mediana de días hábiles por día de entrada
    entry_day_business = (
        union.groupby("day_name")["dia_habil"]
        .median()
        .reindex(day_order)
    )

    # Construir la tabla
    entry_day_summary = pd.DataFrame({
        "day_name": day_order,
        "requests": entry_day_requests.to_numpy(),
        "median_calendar_days": entry_day_calendar.to_numpy(),
        "median_business_days": entry_day_business.to_numpy()
    })


    # Guardar el archivo CSV
    entry_day_summary.to_csv(
        "submission/entry_day_summary.csv",
        index=False
    )

    return channel_summary, yearly_summary, entry_day_summary