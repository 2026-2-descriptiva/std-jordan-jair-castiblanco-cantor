def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """
    
    import json
    from pathlib import Path
    import pandas as pd

    df = pd.read_csv("data/insurance.csv.gz")

    # Identificadores cuasi-identificadores originales
    original_qis = ["age", "sex", "bmi", "children", "region"]
    original_sizes = df.groupby(original_qis, dropna=False).size()

    original_k = int(original_sizes.min())
    original_unique_records = int((original_sizes == 1).sum())

    # Generalizar edad
    df["age_group"] = pd.cut(
        df["age"],
        bins=[18, 30, 40, 50, 65],
        labels=["18-29", "30-39", "40-49", "50-64"],
        right=False
    )

    # Generalizar IMC
    df["bmi_group"] = pd.cut(
        df["bmi"],
        bins=[float("-inf"), 18.5, 25, 30, float("inf")],
        labels=["bajo peso", "normal", "sobrepeso", "obesidad"],
        right=False
    )

    # Generalizar número de hijos
    df["children_group"] = pd.cut(
        df["children"],
        bins=[-1, 0, 2, float("inf")],
        labels=["0", "1-2", "3+"]
    )

    # Definir esquemas
    schemes = {
        "with_children": [
            "age_group", "sex", "bmi_group", "children_group", "region"
        ],
        "without_children": [
            "age_group", "sex", "bmi_group", "region"
        ]
    }

    report_schemes = {}
    published_by_scheme = {}

    # Evaluar esquemas de generalización
    for name, qis in schemes.items():
        class_sizes = df.groupby(
            qis, observed=True, dropna=False
        ).size()

        valid_classes = class_sizes[class_sizes >= 5]

        row_sizes = df.groupby(
            qis, observed=True, dropna=False
        )[qis[0]].transform("size")

        published = df.loc[row_sizes >= 5].copy()
        published_by_scheme[name] = published

        smoker_diversity = published.groupby(
            qis, observed=True, dropna=False
        )["smoker"].nunique()

        classes_without_diversity = smoker_diversity[
            smoker_diversity == 1
        ]

        records_without_diversity = int(
            published.groupby(
                qis, observed=True, dropna=False
            ).size().reindex(classes_without_diversity.index).sum()
        )

        report_schemes[name] = {
            "quasi_identifiers": qis,
            "equivalence_classes": int(len(class_sizes)),
            "k_before_suppression": int(class_sizes.min()),
            "suppressed_records": int(len(df) - len(published)),
            "published_records": int(len(published)),
            "published_classes": int(len(valid_classes)),
            "classes_without_smoker_diversity": int(
                len(classes_without_diversity)
            ),
            "records_without_smoker_diversity": records_without_diversity
        }

    # Seleccionar el esquema que suprime menos registros
    selected_scheme = min(
        report_schemes,
        key=lambda name: report_schemes[name]["suppressed_records"]
    )

    published = published_by_scheme[selected_scheme].copy()
    selected_qis = schemes[selected_scheme]

    # Indicadores originales y publicados
    mean_charges_original = float(df["charges"].mean())
    mean_charges_published = float(published["charges"].mean())

    smoker_rate_original = float((df["smoker"] == "yes").mean())
    smoker_rate_published = float((published["smoker"] == "yes").mean())

    # Construir reporte
    report = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": report_schemes,
        "selected_scheme": selected_scheme,
        "mean_charges_original": mean_charges_original,
        "mean_charges_published": mean_charges_published,
        "smoker_rate_original": smoker_rate_original,
        "smoker_rate_published": smoker_rate_published
    }

    # Guardar entregables
    output_dir = Path("submission")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(
        output_dir / "privacy_report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    published_columns = selected_qis + ["smoker", "charges"]

    published[published_columns].to_csv(
        output_dir / "insurance_published.csv",
        index=False
    )

    return report