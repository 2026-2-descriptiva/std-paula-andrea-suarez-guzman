from ._utils import leer_registros

def pregunta_12():
    sumas = {}
    for registro in leer_registros():
        letra = registro["letter"]
        total = sum(valor for _, valor in registro["metrics"])
        sumas[letra] = sumas.get(letra, 0) + total
    return dict(sorted(sumas.items()))
