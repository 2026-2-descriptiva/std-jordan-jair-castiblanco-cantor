import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Una autoridad aeronáutica publica cada año un ranking de aerolíneas según
    su tasa de demora, y algunas aerolíneas se quejan de que es injusto: las
    demoras se acumulan a lo largo del día, de modo que una aerolínea con
    muchos vuelos en la tarde y la noche parece peor aunque opere igual de
    bien que las demás. Su tarea es construir un ranking que tenga en cuenta
    la mezcla de horarios de cada aerolínea.

    El archivo `data/flights_by_carrier_day_hour.csv.gz` tiene los vuelos
    nacionales entre 2006 y 2008, agregados por año, mes, día de la semana,
    hora programada de salida (`scheduled_departure_hour`) y aerolínea
    (`reporting_airline`). Use las columnas `operated_flights` (vuelos
    operados) y `delayed_departure_15_flights` (vuelos que salieron con 15
    minutos o más de demora).

    Siga estos pasos:

    1. Calcule la tasa nacional de demora de cada hora programada de salida:
       vuelos demorados sobre vuelos operados, con todas las aerolíneas
       juntas.
    2. Para cada aerolínea, calcule las demoras esperadas: en cada hora,
       multiplique sus vuelos operados por la tasa nacional de esa hora, y
       sume sobre todas las horas. Son las demoras que tendría si en cada hora
       se comportara como el promedio nacional.
    3. Divida las demoras observadas entre las esperadas. Un valor mayor que 1
       significa que la aerolínea se demora más de lo que explican sus
       horarios.

    Genere dos archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `hourly_delay_rates.csv`, con una fila por hora, de 0 a 23:
       `scheduled_departure_hour`, `operated_flights`,
       `delayed_departure_15_flights` y `delay_rate`.

    2. `carrier_adjusted_delays.csv`, con una fila por aerolínea:
       `reporting_airline`, `operated_flights`,
       `delayed_departure_15_flights`, `delay_rate` (la tasa sin ajustar),
       `expected_delayed_flights`, `observed_to_expected_ratio`, `crude_rank`
       y `adjusted_rank`. Incluya solamente aerolíneas con al menos 100 000
       vuelos operados. `crude_rank` es la posición según `delay_rate` y
       `adjusted_rank` la posición según `observed_to_expected_ratio`; en
       ambos, 1 es la peor aerolínea. Ordene la tabla por `adjusted_rank`.

    Compare los dos rankings: las aerolíneas que cambian de posición son las
    que el ranking sin ajustar juzga mal por sus horarios.

    La función también debe retornar las dos tablas, en el mismo orden.

    Ejemplo del formato de `carrier_adjusted_delays.csv`:

        reporting_airline,operated_flights,...,crude_rank,adjusted_rank
        EV,819223,...,1,1
        ...
    """

    import pandas as pd


    # Cargar los datos de vuelos por aerolínea, día y hora
    df = pd.read_csv("data/flights_by_carrier_day_hour.csv.gz")

    # Agrupar los vuelos por hora programada de salida
    hourly_delay_rates = (
        df.groupby("scheduled_departure_hour")[
            ["operated_flights", "delayed_departure_15_flights"]
        ]
        .sum()
        .reset_index()
    )

    # Calcular la tasa de demora de cada hora
    hourly_delay_rates["delay_rate"] = (
        hourly_delay_rates["delayed_departure_15_flights"]
        / hourly_delay_rates["operated_flights"]
    )

    hourly_delay_rates.to_csv(
        "submission/hourly_delay_rates.csv",
        index=False
    )  

    # Agrupar vuelos por aerolínea y hora
    agrupacion_ae_hora = (
        df.groupby(["reporting_airline", "scheduled_departure_hour"])[
            ["operated_flights", "delayed_departure_15_flights"]
        ]
        .sum()
        .reset_index()
    )

    # Incorporar la tasa nacional de demora correspondiente a cada hora
    agrupacion_ae_hora = agrupacion_ae_hora.merge(
        hourly_delay_rates[["scheduled_departure_hour", "delay_rate"]],
        on="scheduled_departure_hour",
        how="left"
    )

    # Calcular los vuelos demorados esperados por aerolínea y hora
    agrupacion_ae_hora["expected_delayed_flights"] = (
        agrupacion_ae_hora["operated_flights"]
        * agrupacion_ae_hora["delay_rate"]
    )

    # Agrupar por aerolínea y sumar los valores observados y esperados
    comparacion_ae = (
        agrupacion_ae_hora.groupby("reporting_airline")[
            [
                "operated_flights",
                "delayed_departure_15_flights",
                "expected_delayed_flights"
            ]
        ]
        .sum()
        .reset_index()
    )

    # Conservar aerolíneas con al menos 100.000 vuelos operados
    comparacion_ae = comparacion_ae[
        comparacion_ae["operated_flights"] >= 100000
    ]

    # Calcular la tasa de demora observada por aerolínea
    comparacion_ae["delay_rate"] = (
        comparacion_ae["delayed_departure_15_flights"]
        / comparacion_ae["operated_flights"]
    )

    # Calcular la relación entre demoras observadas y esperadas
    comparacion_ae["observed_to_expected_ratio"] = (
        comparacion_ae["delayed_departure_15_flights"]
        / comparacion_ae["expected_delayed_flights"]
    )

    # Calcular el ranking sin ajustar
    comparacion_ae["crude_rank"] = comparacion_ae["delay_rate"].rank(
        ascending=False
    )

    # Calcular el ranking ajustado
    comparacion_ae["adjusted_rank"] = comparacion_ae[
        "observed_to_expected_ratio"
    ].rank(ascending=False)

    # Ordenar por el ranking ajustado
    comparacion_ae = comparacion_ae.sort_values(
        by="adjusted_rank",
        ascending=True
    )

    # Seleccionar las columnas en el orden solicitado
    comparacion_ae = comparacion_ae[
        [
            "reporting_airline",
            "operated_flights",
            "delayed_departure_15_flights",
            "delay_rate",
            "expected_delayed_flights",
            "observed_to_expected_ratio",
            "crude_rank",
            "adjusted_rank"
        ]
    ]

    # Guardar la segunda tabla sin el índice
    comparacion_ae.to_csv(
        "submission/carrier_adjusted_delays.csv",
        index=False
    )

    # Retornar las dos tablas en el orden del enunciado
    return (
        hourly_delay_rates,
        comparacion_ae
    )    

