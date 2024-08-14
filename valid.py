"""
valid.py:
    En este modulo se realiza la validacion de campos
    de entrada, según el patrón regex indicado.
"""
import re


class Validation:
    def valid_numero(self, numero):
        """
        Valida que el campo 'ID Paciente' (DNI) contenga solo números.

        :Patrón: '^[\d]+$'
        """
        patron = "^[\d]+$"  # r'^[0-9]+$'    # solo numeros
        if re.match(patron, numero) is None:
            return False
        else:
            return True

    def valid_text(self, nombre):
        """
        Valida que los campos 'Nombre y Apellido' y 'Cirujano' contenga solo letras en mayúscula
        y minúscula, sin caracteres especiales. Se permiten acentos, espacios y comas.

        :Patrón: '^[a-zA-Z áéíóú,]+$'
        """
        patron = '^[a-zA-Z áéíóú,]+$'  # solo letras, espacio y acentos
        if re.match(patron, nombre) is None:
            return False
        else:
            return True
