def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """

    import json
    import pandas as pd

    ventas = pd.read_csv("data/ventas.csv.gz")

    # Normalizar nombres de columnas
    nuevos_nombres = []

    for name in ventas.columns:
        name = name.replace("\ufeff", "")
        name = name.strip().lower().replace(" ", "_")
        nuevos_nombres.append(name)

    ventas.columns = nuevos_nombres

    # Columnas requeridas
    requeridas = [
        "supplier_id",
        "supplier",
        "country",
        "city",
        "purchase_date",
        "amount",
        "discount",
        "weight",
        "units",
        "unit_price",
        "contact_email"
    ]

    # Columnas requeridas que faltan
    missing_required_columns = []

    for columna in requeridas:
        if columna not in nuevos_nombres:
            missing_required_columns.append(columna)

    missing_required_columns = sorted(missing_required_columns)

    # Columnas inesperadas
    unexpected_columns = []

    for columna in nuevos_nombres:
        if columna not in requeridas:
            unexpected_columns.append(columna)

    unexpected_columns = sorted(unexpected_columns)

    # Filas completamente duplicadas
    duplicate_row_count = sum(ventas.duplicated())

    # Filas con supplier_id repetido
    conteo_supplier = ventas["supplier_id"].value_counts()

    duplicate_supplier_id_row_count = 0

    for cantidad in conteo_supplier:
        if cantidad > 1:
            duplicate_supplier_id_row_count += cantidad

    # Valores faltantes por columna
    missing_value_count_by_column = ventas.isna().sum().to_dict()

    # Correos inválidos
    invalid_email_count = len(ventas) - sum(
        ventas["contact_email"].str.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        )
    )

    # Unidades inválidas
    invalid_unit_count = 0

    for valor in ventas["units"]:

        if pd.isna(valor):
            continue

        if valor <= 0 or not valor.is_integer():
            invalid_unit_count += 1

    # Valores distintos de país
    country_values = sorted(ventas["country"].unique())

    # Construir reporte
    reporte = {
        "row_count": len(ventas),
        "column_count": len(ventas.columns),
        "missing_required_columns": missing_required_columns,
        "unexpected_columns": unexpected_columns,
        "duplicate_row_count": duplicate_row_count,
        "duplicate_supplier_id_row_count": duplicate_supplier_id_row_count,
        "missing_value_count_by_column": missing_value_count_by_column,
        "invalid_email_count": invalid_email_count,
        "invalid_unit_count": invalid_unit_count,
        "country_values": country_values
    }

    # Guardar reporte en JSON
    with open(
        "submission/data_quality_report.json",
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(reporte, archivo, indent=2)

    return reporte

