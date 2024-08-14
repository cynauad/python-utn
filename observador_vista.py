"""
observador_vista.py:
    Implementacion del patron Observador.

    -	Se crea un observador de la base de datos seleccionada.
    -   La información se almacena en la BBDD.
"""


import datetime
from connector import LogObserver1


class SujetoV:
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


class ConcreteObserverBase(Observador):
    '''Observadores de la clase Vista'''

    def __init__(self, obj):
        self.observador_a = obj
        self.observador_a.agregar(self)

    def update(self, *args):
        base = str(args[0][0])
        # print(base)
        _date = datetime.datetime.now()
        description = "Selected database"
        print(f"{_date}: Selección/Actualización de la base de datos: {base}")

        self.reg = LogObserver1()
        self.reg.date = _date
        self.reg.motivo = description
        self.reg.tipo_base = base
        self.reg.save()
