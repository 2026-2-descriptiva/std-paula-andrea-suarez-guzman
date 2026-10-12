import re
import pandas as pd

def pregunta_01():
    with open("data/clusters_report.txt", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    # Las primeras 4 lineas son el encabezado y la linea de guiones.
    registros = []
    for linea in lineas[4:]:
        if not linea.strip():
            continue
        if re.match(r"^\s*\d+\s", linea):
            cluster, cantidad, porcentaje, _, palabras = linea.split(maxsplit=4)
            registros.append(
                {
                    "cluster": int(cluster),
                    "cantidad_de_palabras_clave": int(cantidad),
                    "porcentaje_de_palabras_clave": float(porcentaje.replace(",", ".")),
                    "principales_palabras_clave": palabras,
                }
            )
        else:
            registros[-1]["principales_palabras_clave"] += " " + linea

    for registro in registros:
        texto = re.sub(r"\s+", " ", registro["principales_palabras_clave"])
        texto = texto.strip().rstrip(".")
        palabras = [palabra.strip() for palabra in texto.split(",")]
        registro["principales_palabras_clave"] = ", ".join(palabras)

    return pd.DataFrame(registros)
