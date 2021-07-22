import sqlite3
from myCripto import app


class DBmanager():

    def __init__(self, ruta_base_datos):
        self.db_path = ruta_base_datos


    def __toDict__(self, cur):
        claves = cur.description
        filas = cur.fetchall()
        
        movimientos = []
        for fila in filas:
            d = {}
            for tclave, valor in zip(claves, fila):
                d[tclave[0]]= valor
            movimientos.append(d)

        
        return movimientos

    def consultaSQL(self, query, parametros=[]):
        conexion = sqlite3.connect(self.db_path)
        cur = conexion.cursor()

        cur.execute(query, parametros)
        movimientos = self.__toDict__(cur)
        conexion.close()
        return movimientos

    def modificaTablaSQL(self, query, parametros=[]):
        conexion = sqlite3.connect(self.db_path)
        cur = conexion.cursor()

        cur.execute(query, parametros)
        conexion.commit()
        conexion.close()
