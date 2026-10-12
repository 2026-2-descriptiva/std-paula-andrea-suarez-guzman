from ._utils import leer_registros

def pregunta_09():
    conteo = {}
    for registro in leer_registros():
        for clave, _ in registro["metrics"]:
            conteo[clave] = conteo.get(clave, 0) + 1
    return dict(sorted(conteo.items()))
