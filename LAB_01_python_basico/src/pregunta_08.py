from ._utils import leer_registros

def pregunta_08():
    letras = {}
    for registro in leer_registros():
        letras.setdefault(registro["value"], set()).add(registro["letter"])
    return [(valor, sorted(conjunto)) for valor, conjunto in sorted(letras.items())]
