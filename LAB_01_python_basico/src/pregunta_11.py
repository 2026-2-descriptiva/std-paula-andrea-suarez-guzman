from ._utils import leer_registros

def pregunta_11():
    sumas = {}
    for registro in leer_registros():
        for letra in registro["codes"]:
            sumas[letra] = sumas.get(letra, 0) + registro["value"]
    return dict(sorted(sumas.items()))
