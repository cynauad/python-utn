"""
model.py:

    Se encuentran las acciones las principales funciones de Alta, Baja,
    Modificación y Consulta (buscar) de la datos de la base.

    Las querys se gestionan con el ORM Peewee. *En cada método se describe la query SQL que estaría ejecutando*. 

"""

# #######################################################
#         MODELO (FUNCIONES)
# #######################################################

from connector import Cirugias, select_database
import pandas as pd
from decoradores import log_event
from observador_model import SujetoM


class Abmc(SujetoM):    # ABMC es el tema a controlar por el Sujeto
    def __init__(self, database):  # se definen atributos
        select_database(database)
        self.cirugia = Cirugias()

    @log_event
    def alta(self, dato, ):
        """Se almacena la información en la BBDD. Al llamar a la funcion requiere que se le envie la data a ingresar.

        Ejemplo Sql:

        *INSERT INTO eventos_quirugicos(id_pac, name, procedure, surgeon, date, hour, duration)  VALUES (?,?,?,?,?,?,?)*"""
        self.cirugia.id_pac = dato[0]
        self.cirugia.name = dato[1]
        self.cirugia.surgeon = dato[2]
        self.cirugia.procedure = dato[3]
        self.cirugia.date = dato[4]
        self.cirugia.hour = dato[5]
        self.cirugia.duration = dato[6]
        self.cirugia.save()
        ingreso = Cirugias.get(Cirugias.id_pac == dato[0])
        self.notificar('alta', "ID_cx: %s" % dato[0], ingreso)           # llamo a notificar del sujeto

    def update_tree(self):
        """Consulta la BBDD para mostrar todo el contenido.

        Ejemplo Sql:

        *SELECT * FROM eventos_quirugicos ORDER BY id_cx DESC*

            **Return:** retorna toda la información."""
        resultado = self.cirugia.select()
        return resultado

    @log_event
    def borrar(self, data):
        """Se elimina el registro deseado.

        Ejemplo Sql:

        *DELETE FROM eventos_quirugicos WHERE id_cx = ?*"""
        borrado = Cirugias.get(Cirugias.id_cx == data)
        borrado.delete_instance()
        self.notificar("Baja", "ID_pac: %s" % data, borrado)

    def consulta(self, data):
        """Se realiza el select para consultar la información deseada.

        Ejemplo Sql:

        *SELECT * from eventos_quirugicos WHERE id_pac = ?*

           **Return:** retorna la información de un id seleccionado.
        """
        seleccion = Cirugias.get(Cirugias.id_pac == data)
        print(seleccion)
        return seleccion

    @log_event
    def guardar(self, dato, mi_id):
        """Se actualiza la información deseada en la BBDD.

        Ejemplo Sql:

        *UPDATE eventos_quirugicos SET (id_pac, name, procedure, surgeon, date, hour, duration) = (?,?,?,?,?,?,?) WHERE id_cx= mi_id*
        """
        print(dato)
        print(mi_id)
        actualizar = Cirugias.update(id_pac=dato[0], name=dato[1],
                                     surgeon=dato[2], procedure=dato[3],
                                     date=dato[4], hour=dato[5],
                                     duration=dato[6]).where(
                                         Cirugias.id_cx == mi_id)
        actualizar.execute()

    def export(self, ):
        """Se realiza el select para consultar la BBDD.
        Se guarda en un dataframe para luego exportarlo a .xlsx

        Ejemplo Sql:

        *SELECT * FROM eventos_quirugicos ORDER BY id_cx ASC*
        """
        resultado = Cirugias.select()
        datos_dict = [{campo: getattr(objeto, campo)
                       for campo in Cirugias._meta.fields} for objeto in resultado]
        ''''Codigo para exportar a excel con pandas'''
        df = pd.DataFrame(datos_dict)
        # print(df.head(1))
        df.to_excel('export_db.xlsx')
