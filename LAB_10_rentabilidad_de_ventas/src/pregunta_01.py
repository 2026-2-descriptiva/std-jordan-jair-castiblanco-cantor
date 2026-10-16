import pandas as pd

def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
   Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa. <
    - `loss_line_rate`: la proporción de líneas con pérdida. <
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida, <
      escrita como número positivo. <
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """

    df = pd.read_csv(
        "data/superstore_orders.csv.gz",
        sep=";",
        decimal=",",
        compression="gzip"
    )

    # Indicador 1: cantidad de líneas de pedido
    lines = len(df)

    # Indicador 2: cantidad de pedidos distintos
    orders = df["Order ID"].nunique()

    # Indicador 3: ventas totales
    sales = df["Sales"].sum()

    # Indicador 4: ganancia total
    profit = df["Profit"].sum()

    # Indicador 5: margen de rentabilidad
    profit_margin = profit / sales

    # Indicador 6: cantidad de líneas con pérdidas
    loss_lines = (df["Profit"] < 0).sum()

    # Indicador 7: proporción de líneas con pérdidas
    loss_line_rate = loss_lines / lines

    # Indicador 8: valor total de las pérdidas
    lost_profit = abs(df.loc[df["Profit"] < 0, "Profit"].sum())

    # Resumen general de rentabilidad
    profitability_summary = {
        "lines": lines,
        "orders": orders,
        "sales": sales,
        "profit": profit,
        "profit_margin": profit_margin,
        "loss_lines": loss_lines,
        "loss_line_rate": loss_line_rate,
        "lost_profit": lost_profit
    }

    profitability_summary = pd.DataFrame(
        profitability_summary,
        index=[0]
    )

    # Guardar el resumen general
    profitability_summary.to_csv(
        "submission/profitability_summary.csv",
        index=False
    )

    # Clasificación por banda de descuento
    df.loc[df["Discount"] == 0, "discount_band"] = "0%"

    df.loc[
        (df["Discount"] > 0) & (df["Discount"] <= 0.05),
        "discount_band"
    ] = "1%-5%"

    df.loc[
        (df["Discount"] > 0.05) & (df["Discount"] <= 0.10),
        "discount_band"
    ] = "6%-10%"

    df.loc[df["Discount"] > 0.10, "discount_band"] = "más de 10%"

    # Indicadores por banda
    discount_summary = df.groupby("discount_band").size().rename("lines")
    sales_dis = df.groupby("discount_band")["Sales"].sum().rename("sales")
    profit_dis = df.groupby("discount_band")["Profit"].sum().rename("profit")

    # Margen de rentabilidad por banda
    profit_margin_dis = (profit_dis / sales_dis).rename("profit_margin")

    # Líneas con pérdidas por banda
    df["loss_line"] = df["Profit"] < 0

    loss_lines_dis = (
        df.groupby("discount_band")["loss_line"]
        .sum()
    )

    # Proporción de líneas con pérdidas por banda
    loss_line_rate_dis = (
        loss_lines_dis / discount_summary
    ).rename("loss_line_rate")

    # Valor de las pérdidas por banda, expresado en positivo
    lost_profit_dis = (
        df.loc[df["Profit"] < 0]
        .assign(lost_profit=lambda x: -x["Profit"])
        .groupby("discount_band")["lost_profit"]
        .sum()
        .rename("lost_profit")
    )

    # Unir indicadores en una tabla
    discount_summary = pd.concat(
        [
            discount_summary,
            sales_dis,
            profit_dis,
            profit_margin_dis,
            loss_line_rate_dis,
            lost_profit_dis
        ],
        axis=1
    ).reset_index()

    # Mantener el orden solicitado para las bandas
    orden_bandas = ["0%", "1%-5%", "6%-10%", "más de 10%"]

    discount_summary["discount_band"] = pd.Categorical(
        discount_summary["discount_band"],
        categories=orden_bandas,
        ordered=True
    )

    discount_summary = discount_summary.sort_values(
        "discount_band"
    ).reset_index(drop=True)

    # Completar pérdidas faltantes con cero
    discount_summary["lost_profit"] = (
        discount_summary["lost_profit"].fillna(0)
    )

    # Seleccionar las columnas y el orden solicitado
    discount_summary = discount_summary[
        [
            "discount_band",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "loss_line_rate",
            "lost_profit"
        ]
    ]

    # Guardar resumen por banda de descuento
    discount_summary.to_csv(
        "submission/discount_summary.csv",
        index=False
    )

    # 3. Agrupar por segmento de cliente y categoría de producto
    priority_segments_group = df.groupby(
        ["Customer Segment", "Product Category"]
    )

    # Contar las líneas por combinación
    segment_lines = priority_segments_group.size().rename("lines")

    # Conservar grupos con al menos 100 líneas
    segment_lines = segment_lines[segment_lines >= 100]

    # Filtrar el DataFrame original
    priority_df = df[
        df.set_index(
            ["Customer Segment", "Product Category"]
        ).index.isin(segment_lines.index)
    ]

    # Calcular ventas por combinación
    segment_sales = (
        priority_df.groupby(
            ["Customer Segment", "Product Category"]
        )["Sales"].sum().rename("sales")
    )

    # Calcular beneficio por combinación
    segment_profit = (
        priority_df.groupby(
            ["Customer Segment", "Product Category"]
        )["Profit"].sum().rename("profit")
    )

    # Calcular margen de rentabilidad
    segment_profit_margin = (
        segment_profit / segment_sales
    ).rename("profit_margin")

    # Calcular pérdidas por combinación, expresadas en positivo
    segment_lost_profit = (
        priority_df.loc[priority_df["Profit"] < 0]
        .assign(lost_profit=lambda x: -x["Profit"])
        .groupby(
            ["Customer Segment", "Product Category"]
        )["lost_profit"]
        .sum()
    )

    # Unir los indicadores en una sola tabla
    priority_segments = pd.concat(
        [
            segment_lines,
            segment_sales,
            segment_profit,
            segment_profit_margin,
            segment_lost_profit
        ],
        axis=1
    ).reset_index()

    # Reemplazar pérdidas faltantes por cero
    priority_segments["lost_profit"] = (
        priority_segments["lost_profit"].fillna(0)
    )

    # Ordenar de mayor a menor pérdida y conservar las cinco primeras
    priority_segments = priority_segments.sort_values(
        "lost_profit",
        ascending=False
    ).head(5)

    # Organizar las columnas
    priority_segments = priority_segments[
        [
            "Customer Segment",
            "Product Category",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "lost_profit"
        ]
    ].reset_index(drop=True)

    # Guardar resumen de los cinco segmentos prioritarios
    priority_segments.to_csv(
        "submission/priority_segments.csv",
        index=False
    )

    # Retornar las tres tablas en el orden solicitado
    return (
        profitability_summary,
        discount_summary,
        priority_segments
    )


pregunta_01()