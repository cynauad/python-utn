"""
decoradores.py:
    En este modulo se arman los decoradores que se utilizaran para
    el registro de logs.
"""

import datetime


def log_event(function):
    def envolver(*args, **kwargs):
        resultado = function(*args, **kwargs)
        # # muentro en pantalla los eventos
        print("---"*5) 
        if function.__name__ == 'alta':
            mensaje = (f'''{datetime.datetime.now()}: Evento registrado: "{function.__name__}". Datos: {args[1]}''')
            print(mensaje)
        elif function.__name__ == 'guardar':
            mensaje = (f'''{datetime.datetime.now()}: Evento registrado: "{function.__name__}". ID = {args[-1]} se ha modificado con los
                    datos = {args[1]}''')
            print(mensaje)
        else:
            mensaje = (f'''{datetime.datetime.now()}: Evento registrado: "{function.__name__}". El ID = {args[-1]} se ha eliminado''')
            print(mensaje)

        # genero un .txt para guardar el registro de logs
        archivo = open('logs_loggins.txt', 'a')
        archivo.write(mensaje + "\n")
        archivo.close()
        return resultado
    return envolver
