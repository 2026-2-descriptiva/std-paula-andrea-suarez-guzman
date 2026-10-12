"""Funciones auxiliares para leer `data/data.csv.gz`."""

import gzip


def leer_registros(ruta="data/data.csv.gz"):
    """Lee el archivo y retorna una lista de diccionarios, uno por registro."""

    registros = []
    with gzip.open(ruta, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            letter, value, date, codes, metrics = linea.split("\t")
            registros.append(
                {
                    "letter": letter,
                    "value": int(value),
                    "date": date,
                    "codes": codes.split(","),
                    "metrics": [
                        (clave, int(valor))
                        for clave, valor in (
                            par.split(":") for par in metrics.split(",")
                        )
                    ],
                }
            )
    return registros