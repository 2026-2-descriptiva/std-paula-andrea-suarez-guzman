from ._utils import leer_registros

def pregunta_07():
    letras = {}
    for registro in leer_registros():
        letras.setdefault(registro["value"], []).append(registro["letter"])
    return sorted(letras.items())
