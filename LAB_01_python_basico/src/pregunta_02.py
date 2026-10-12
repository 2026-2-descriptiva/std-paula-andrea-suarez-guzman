from ._utils import leer_registros

def pregunta_02():
    conteo = {}
    for registro in leer_registros():
        letra = registro["letter"]
        conteo[letra] = conteo.get(letra, 0) + 1
    return sorted(conteo.items())
