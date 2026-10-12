from ._utils import leer_registros

def pregunta_01():
    registros = leer_registros()
    return sum(registro["value"] for registro in registros)
