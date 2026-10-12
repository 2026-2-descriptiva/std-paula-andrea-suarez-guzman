from ._utils import leer_registros

def pregunta_06():
    valores = {}
    for registro in leer_registros():
        for clave, valor in registro["metrics"]:
            valores.setdefault(clave, []).append(valor)
    return [(clave, min(lista), max(lista)) for clave, lista in sorted(valores.items())]
