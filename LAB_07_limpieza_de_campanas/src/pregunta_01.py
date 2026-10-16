import pandas as pd
from pathlib import Path

def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.
       

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """

    # Leer e integrar los diez archivos comprimidos
    files = sorted(Path("data").glob("bank-marketing-campaing-*.csv.gz"))

    df = pd.concat(
        [pd.read_csv(file) for file in files],
        ignore_index=True
    )

    # Convertir los meses a números
    months = {
        "jan": "01", "feb": "02", "mar": "03",
        "apr": "04", "may": "05", "jun": "06",
        "jul": "07", "aug": "08", "sep": "09",
        "oct": "10", "nov": "11", "dec": "12"
    }

    df["month"] = df["month"].map(months)

    # Construir la fecha con el año 2022
    df["last_contact_date"] = (
        "2022-" + df["month"] + "-" +
        df["day"].astype(str).str.zfill(2)
    )

    # Limpiar job
    df["job"] = df["job"].str.replace(".", "", regex=False)
    df["job"] = df["job"].str.replace("-", "_", regex=False)

    # Limpiar education
    df["education"] = df["education"].str.replace(".", "_", regex=False)
    df["education"] = df["education"].replace("unknown", pd.NA)

    # Convertir variables del cliente a valores binarios
    df["credit_default"] = (df["credit_default"] == "yes").astype(int)
    df["mortgage"] = (df["mortgage"] == "yes").astype(int)


    # Convertir resultados de campaña a valores binarios
    df["previous_outcome"] = (
        df["previous_outcome"] == "success"
    ).astype(int)

    df["campaign_outcome"] = (
        df["campaign_outcome"] == "yes"
    ).astype(int)

    # Crear la tabla de clientes
    client = df[[
        "client_id",
        "age",
        "job",
        "marital",
        "education",
        "credit_default",
        "mortgage"
    ]].copy()

    # Crear la tabla de campañas
    campaign = df[[
        "client_id",
        "number_contacts",
        "contact_duration",
        "previous_campaign_contacts",
        "previous_outcome",
        "campaign_outcome",
        "last_contact_date"
    ]].copy()

    # Crear la tabla económica
    economics = df[[
        "client_id",
        "cons_price_idx",
        "euribor_three_months"
    ]].copy()

    # Crear la carpeta de salida si no existe
    output_dir = Path("submission")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Guardar los archivos CSV sin índice
    client.to_csv(output_dir / "client.csv", index=False)
    campaign.to_csv(output_dir / "campaign.csv", index=False)
    economics.to_csv(output_dir / "economics.csv", index=False)

    # Devolver los tres DataFrames
    # return client, campaign, economics

    