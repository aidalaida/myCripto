from myCripto.dataaccess import *
dbManager = DBmanager()

def calcular_saldo(cripto):
    saldo = 0
    query = "SELECT * From myCRYPTO WHERE criptoTo=?;"
    parametros = [cripto]
    movimientosCompras = dbManager.consultaSQL(query, parametros)

    query = "SELECT * From myCRYPTO WHERE criptoF=?;"
    parametros = [cripto]
    movimientosVentas = dbManager.consultaSQL(query, parametros)

    for movimiento in movimientosCompras:
        saldo += movimiento['Qto']
    for movimiento in movimientosVentas:
        saldo -= movimiento['Qfrom']

    return saldo

def eurosInvertidos(cripto): 
    saldo = 0
    query = "SELECT * From myCRYPTO WHERE criptoF=?;"
    parametros = [cripto]
    movimientosCompras = dbManager.consultaSQL(query, parametros)
    
    for movimiento in movimientosCompras:
        saldo += movimiento['Qfrom']
    
    return saldo