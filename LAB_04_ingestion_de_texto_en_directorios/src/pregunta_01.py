def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV. 

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """

    import glob
    import os.path
    import pandas as pd

    if not os.path.exists("submission"):
        os.makedirs("submission")

    for division in ["train", "test"]:

        registros = []

        carpetas = sorted(glob.glob(f"data/{division}/*"))

        for carpeta in carpetas:

            target = os.path.basename(carpeta)

            archivos = sorted(glob.glob(f"{carpeta}/*.txt"))

            for archivo in archivos:

                with open(archivo, "r", encoding="utf-8") as f:
                    phrase = f.read().strip()

                registro = {
                    "phrase": phrase,
                    "target": target
                }

                registros.append(registro)

        df = pd.DataFrame(registros)

        df.to_csv(f"submission/{division}_dataset.csv", index=False)
