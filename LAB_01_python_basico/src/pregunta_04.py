from ._utils import leer_registros

def pregunta_04():
    conteo = {}
    for registro in leer_registros():
        mes = registro["date"].split("-")[1]
        conteo[mes] = conteo.get(mes, 0) + 1
    return sorted(conteo.items())
