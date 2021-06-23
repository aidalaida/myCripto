import sqlite3

class DBmanager():

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
        conexion = sqlite3.connect("movimientosCripto.db")
        cur = conexion.cursor()

        cur.execute(query, parametros)
        movimientos = self.__toDict__(cur)
        conexion.close()
        return movimientos

    def modificaTablaSQL(self, query, parametros=[]):
        conexion = sqlite3.connect("movimientosCripto.db")
        cur = conexion.cursor()

        cur.execute(query, parametros)
        conexion.commit()
        conexion.close()
