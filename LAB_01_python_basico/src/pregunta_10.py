from ._utils import leer_registros

def pregunta_10():
    return [
        (registro["letter"], len(registro["codes"]), len(registro["metrics"]))
        for registro in leer_registros()
    ]
