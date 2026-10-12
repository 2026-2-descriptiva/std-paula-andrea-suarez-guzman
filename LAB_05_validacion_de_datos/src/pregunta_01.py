import json
from pathlib import Path

import pandas as pd

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

    columnas_requeridas = [
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
        "contact_email",
    ]

    # Se lee todo como texto para no alterar ningun valor del archivo.
    df = pd.read_csv(
        "data/ventas.csv.gz",
        dtype=str,
        keep_default_na=False,
        encoding="utf-8-sig",
    )
    df.columns = [
        columna.replace("\ufeff", "").strip().lower().replace(" ", "_")
        for columna in df.columns
    ]

    faltantes = df.apply(lambda columna: columna.str.strip().isin(["", "N/A"]))

    correos = df["contact_email"].str.strip()
    correo_valido = correos.str.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s.]+")
    correos_invalidos = ~correo_valido & ~faltantes["contact_email"]

    unidades = pd.to_numeric(df["units"].str.strip(), errors="coerce").dropna()
    unidades_invalidas = (unidades <= 0) | (unidades % 1 != 0)

    reporte = {
        "row_count": int(len(df)),
        "column_count": int(df.shape[1]),
        "missing_required_columns": sorted(
            set(columnas_requeridas) - set(df.columns)
        ),
        "unexpected_columns": sorted(set(df.columns) - set(columnas_requeridas)),
        "duplicate_row_count": int(df.duplicated().sum()),
        "duplicate_supplier_id_row_count": int(
            df["supplier_id"].str.strip().duplicated(keep=False).sum()
        ),
        "missing_value_count_by_column": {
            columna: int(cantidad) for columna, cantidad in faltantes.sum().items()
        },
        "invalid_email_count": int(correos_invalidos.sum()),
        "invalid_unit_count": int(unidades_invalidas.sum()),
        "country_values": sorted(df["country"].unique().tolist()),
    }

    salida = Path("submission")
    salida.mkdir(parents=True, exist_ok=True)
    with open(salida / "data_quality_report.json", "w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, ensure_ascii=False, indent=2)

    return reporte
