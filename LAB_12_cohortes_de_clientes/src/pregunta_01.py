import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    # Cargar los datos
    df = pd.read_csv("data/sales.csv.gz")

    # Convertir OrderDate a tipo fecha
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])

    # Obtener la primera fecha de compra de cada cliente
    group_cohorte = df.groupby("CustomerID")["OrderDate"].min()

    # Obtener el mes de primera compra de cada cliente
    group_cohorte = group_cohorte.dt.strftime("%Y-%m")

    # Preparar la tabla de cohortes para la unión
    group_cohorte = group_cohorte.rename("cohort_month").reset_index()

    # Incorporar la cohorte a cada orden
    union = df.merge(
        group_cohorte,
        on="CustomerID",
        how="left"
    )

    # Convertir el mes de la cohorte a fecha
    union["cohort_month"] = pd.to_datetime(union["cohort_month"])

    # Calcular los meses absolutos
    order_month = (
        union["OrderDate"].dt.year * 12
        + union["OrderDate"].dt.month
    )

    cohort_month = (
        union["cohort_month"].dt.year * 12
        + union["cohort_month"].dt.month
    )

    # Calcular los meses transcurridos desde la primera compra
    union["period_index"] = order_month - cohort_month

    # Contar clientes distintos por cohorte y período
    active_customers = (
        union.groupby(["cohort_month", "period_index"])["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )

    # Obtener el tamaño inicial de cada cohorte
    cohort_size = active_customers[
        active_customers["period_index"] == 0
    ]

    # Conservar las columnas necesarias
    cohort_size = cohort_size[["cohort_month", "active_customers"]]

    # Renombrar el conteo como tamaño de cohorte
    cohort_size = cohort_size.rename(
        columns={"active_customers": "cohort_size"}
    )

    # Incorporar el tamaño inicial de cada cohorte
    active_customers = active_customers.merge(
        cohort_size,
        on="cohort_month",
        how="left"
    )

    # Calcular tasa de retención
    active_customers["retention_rate"] = (
        active_customers["active_customers"]
        / active_customers["cohort_size"]
    )

    # Ordenar por cohorte y período
    cohort_retention = active_customers.sort_values(
        by=["cohort_month", "period_index"],
        ascending=True
    )

    # Convertir el mes de cohorte al formato AAAA-MM
    cohort_retention["cohort_month"] = (
        cohort_retention["cohort_month"].dt.strftime("%Y-%m")
    )

    # Seleccionar las columnas solicitadas
    cohort_retention = cohort_retention[[
        "cohort_month",
        "period_index",
        "active_customers",
        "cohort_size",
        "retention_rate"
    ]]

    # Guardar la tabla sin el índice de Pandas
    cohort_retention.to_csv(
        "submission/cohort_retention.csv",
        index=False
    )

    # Transformar la tabla larga en una matriz para el mapa
    heatmap_data = cohort_retention.pivot(
        index="cohort_month",
        columns="period_index",
        values="retention_rate"
    )

    # Crear la figura
    plt.figure(figsize=(12, 8))

    # Dibujar el mapa de calor
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt= ".0%",
        mask=heatmap_data.isna()
    )

    plt.title("Retención de clientes por cohorte")
    plt.xlabel("Meses desde la primera compra")
    plt.ylabel("Mes de primera compra")

    # Guardar el mapa de calor
    plt.savefig(
        "submission/cohort_retention_heatmap.png"
    )

    # Cerrar la figura
    #plt.close()

    return cohort_retention