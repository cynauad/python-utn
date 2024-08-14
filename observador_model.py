"""
observador_model.py:
    Implementacion del patron Observador.

    -	Se crea un observador de los métodos Alta y Baja.
    -   La información se almacena en la BBDD.
"""

import datetime
from connector import LogObserver2


class SujetoM:
    '''Almacena quienes son los observadores'''
    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def quitar(self, obj):
        pass

    def notificar(self, *args):
        for observador in self.observadores:
            observador.update(args)


class Observador:
    def update(self,):
        raise NotImplementedError("Delegación de actualización")


class ConcreteObserverMetodo(Observador):
    '''Observadores de la clase Model'''

    def __init__(self, obj):
        self.observador_b = obj
        self.observador_b.agregar(self)

    def update(self, *args):
        _date = datetime.datetime.now()
        desc = str(args[0][2])
        print(f"{_date}: Actualización del método: ", str(args[0]))

        self.reg2 = LogObserver2()
        self.reg2.date = _date
        self.reg2.metodo = args[0][0]
        self.reg2.identificador = args[0][1]
        self.reg2.description = desc
        self.reg2.save()