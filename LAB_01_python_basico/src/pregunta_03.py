from ._utils import leer_registros

def pregunta_03():
    sumas = {}
    for registro in leer_registros():
        letra = registro["letter"]
        sumas[letra] = sumas.get(letra, 0) + registro["value"]
    return sorted(sumas.items())
