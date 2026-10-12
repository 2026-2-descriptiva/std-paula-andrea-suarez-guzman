from ._utils import leer_registros

def pregunta_05():
    valores = {}
    for registro in leer_registros():
        valores.setdefault(registro["letter"], []).append(registro["value"])
    return [(letra, max(lista), min(lista)) for letra, lista in sorted(valores.items())]
