from pathlib import Path

import pandas as pd

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

    df = pd.read_csv(
        "data/solicitudes_de_credito.csv.gz",
        sep=";",
        index_col=0,
    )

    # Campos de texto: minusculas y palabras separadas por un solo espacio.
    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for columna in columnas_texto:
        df[columna] = (
            df[columna]
            .str.lower()
            .str.replace(r"[-_]", " ", regex=True)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    # Estrato: "02" y 2 representan lo mismo.
    df["estrato"] = df["estrato"].astype(int)

    # Monto: quitar "$", espacios, separadores de miles y decimales ".00".
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.strip()
        .str.replace(r"\.00$", "", regex=True)
        .str.replace(r"[^0-9]", "", regex=True)
        .astype(int)
    )

    # Fechas: vienen como DD/MM/AAAA o como AAAA/MM/DD.
    fechas = df["fecha_de_beneficio"].astype(str).str.strip()
    df["fecha_de_beneficio"] = pd.to_datetime(
        fechas, format="%d/%m/%Y", errors="coerce"
    ).fillna(pd.to_datetime(fechas, format="%Y/%m/%d", errors="coerce"))
    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].dt.strftime("%Y-%m-%d")

    # Comuna: los faltantes son parte de los datos y se conservan.
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype("Int64")

    # Registros incompletos (sin contar la comuna) y duplicados.
    columnas_obligatorias = [c for c in df.columns if c != "comuna_ciudadano"]
    df = df.dropna(subset=columnas_obligatorias)
    df = df.drop_duplicates()

    salida = Path("submission")
    salida.mkdir(parents=True, exist_ok=True)
    df.to_csv(salida / "solicitudes_de_credito.csv", sep=";", index=False)
