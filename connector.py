"""
connector.py:
    Se definen las conexiones a bases de datos y creacion de tablas.
"""

from peewee import SqliteDatabase, PostgresqlDatabase, Model, AutoField
from peewee import IntegerField, CharField, DateTimeField, TimeField


# --------- LEER:   está por defecto usar Sqlit3. -----------


default = SqliteDatabase("base_quirurgica_sqlite.db")


def select_database(db):
    """Permite setear la base de datos seleccionada.
    Actualmente, se setea por defecto Sqlite3.
    """
    global default
    if db == "PostgreSQL":
        default = PostgresqlDatabase('baseQ_postgres', user='postgres',
                                     password='postgres', host='localhost',
                                     port=5432)
    else:
        print("conectado a Sqlite")
        # default = SqliteDatabase('base_quirurgica_sqlite.db')


class BaseModel(Model,):              # crea la base
    """Se crea la base"""   
    class Meta:
        database = default     # se selecciona en pantalla


class Cirugias(BaseModel):             # crea la tabla
    """Se crea la tabla, con los siguientes campos:""" 
    id_cx = AutoField()
    id_pac = IntegerField(unique=True)
    name = CharField()
    surgeon = CharField()
    procedure = CharField()
    date = DateTimeField()
    hour = TimeField()
    duration = IntegerField()

    def __str__(self,):
        return "Cx de "+self.procedure+" para el paciente "+self.name+", con fecha: "+self.date+" y cirujano: "+self.surgeon


class LogObserver1(BaseModel):
    """Se crea la tabla para el registro del observador de la base de datos:"""
    date = DateTimeField()
    motivo = CharField()
    tipo_base = CharField()


class LogObserver2(BaseModel):
    """Se crea la tabla para el registro del observador del modelo:"""
    date = DateTimeField()
    metodo = CharField()
    identificador = CharField()
    description = CharField()


default.connect()
default.create_tables([Cirugias, LogObserver1, LogObserver2])
