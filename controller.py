"""
controller.py:
    En el patron MVC, esta clase es el controlador de la App.

    -	Contiene la inicializacion de la app.
    -	Contiene un patrón observador que informa cambios en la base de datos seleccionada.
"""

# ===============================================================================
#
#           Creación de un CRUD para Agenda de Eventos Quirúrgicos
#
# ===============================================================================
#                         Estudiante: CYNTHIA AUAD
#                           Docente: Juan Barreto
#
#                   Diplomatura en Python - Nivel Avanzado
#                    UTN – Facultad Regional Buenos Aires
# -------------------------------------------------------------------------------


from tkinter import Tk
import vista

from observador_vista import ConcreteObserverBase

__author__ = "Cynthia Auad"
__email__ = "auad03@gmail.com"
__copyright__ = "Copyright 2024"
__version__ = "0.1"

# ##############################################
#        CONTROLADOR
# ##############################################


class Controller:
    '''
    Clase principal de la aplicación.
    '''

    def __init__(self, root):    # todo sucede dentro del constructor
        """
        Se inicia la aplicación.
        Se inicia la instancia del patrón observador
        """

        self.root_controller = root
        self.objeto_vista = vista.Vista(self.root_controller)  # aca le paso master
        self.objeto_observador_base = ConcreteObserverBase(self.objeto_vista) # instancio el observador
        #  y le digo que siga a la instancia de Vista que me permite seleccionar la base de datos


if __name__ == "__main__":
    master = Tk()
    Controller(master)

    master.mainloop()
