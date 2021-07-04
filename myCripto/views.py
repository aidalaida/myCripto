from os import putenv
from flask_wtf import form
from myCripto import app
from flask import jsonify, render_template, request, redirect, url_for, flash
from myCripto import forms
from myCripto.forms import criptosForm
from datetime import date
from datetime import datetime
from myCripto.dataaccess import *
import requests
import json

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


@app.route('/')
def index():
    query = "SELECT * From myCRYPTO;"
    parametros = []
    movimientos = dbManager.consultaSQL(query, parametros)

    return render_template('inicio.html', datos = movimientos)

@app.route('/inicio')
def inicio():
    pantallaInicio = index()
    return pantallaInicio


@app.route('/purchase', methods=['GET', 'POST'])
def comprar():
    
    formulario = criptosForm()

    if request.method == 'GET':
        return render_template('comprar.html', form = formulario)
    else:
        if formulario.submit.data == True:
            if formulario.validate():
                
                query = "INSERT INTO myCRYPTO (fecha, hora, criptoF, Qfrom, criptoTo, Qto) VALUES (?, ?, ?, ?, ?, ?)"
                try:
                    fecha = datetime.now().strftime('%Y-%m-%d')
                    hora = datetime.now().strftime('%H:%M:%S')


                    dbManager.modificaTablaSQL(query, [fecha, hora, formulario.criptoF.data, formulario.Qfrom.data, formulario.criptoTo.data, formulario.Qto.data])
                    
            
                except sqlite3.Error as el_error:
                    print("Error en SQL INSERT", el_error)
                    flash("Se ha producido un error en la base de datos. Pruebe en unos minutos", "error")
                    return render_template('inicio.html', form=formulario)

                return redirect(url_for("index"))
            else:
                return render_template('comprar.html', form = formulario)

        elif formulario.calcular.data == True:
            criptoF = formulario.criptoF.data
            Qfrom = formulario.Qfrom.data
            criptoTo = formulario.criptoTo.data

            query = "SELECT * From myCRYPTO;"
            parametros = []
            movimientos = dbManager.consultaSQL(query, parametros)

            if not movimientos or criptoF == 'EUR':
                if criptoF != 'EUR':
                    flash ("En la primera compra solo se pueden utilizar Euros")
                    return render_template('comprar.html', form = formulario)
                            
                elif criptoF == criptoTo:
                    flash ("No se puede utilizar la misma moneda")
                    return render_template('comprar.html', form = formulario)
                elif type(Qfrom) is not float:
                    flash ("La cantidad introducida debe ser un número. Recuerda que los decimales hay que escribirlos con punto")
                    return render_template('comprar.html', form = formulario)
                
                elif Qfrom < 0:
                    flash ("La cantidad introducida no puede ser un número negativo")
                    return render_template('comprar.html', form = formulario)
                
                else:
                
                    url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY=d6a12093-2975-407e-8c90-8b73b5be116a"

                    resultado = requests.get(url.format(Qfrom, criptoF, criptoTo))
                    if resultado.status_code == 200:
                    
                        criptoMonedas = resultado.json()
                            
                        if criptoMonedas ["status"]["error_code"] != 0:
                            flash("Error en la API: " + criptoMonedas["status"]["error_message"])
                            return render_template('comprar.html', form = formulario)
                        
                        
                        cantidadTo = criptoMonedas["data"]["quote"][criptoTo]["price"]
                        formulario.Qto.data = cantidadTo
                        pu = Qfrom / formulario.Qto.data
                        formulario.PU.data = pu
                        
                        return render_template('comprar.html', form = formulario, cantidadTo = cantidadTo, pu=pu)

                    else:
                        flash("Error en el acceso a la API, intentarlo de nuevo más tarde")
                        return render_template('comprar.html', form = formulario)
            else:
                query = "SELECT * From myCRYPTO WHERE criptoTo=?;"
                parametros = [criptoF]
                movimientos = dbManager.consultaSQL(query, parametros)

                if criptoF == criptoTo:
                    flash ("No se puede utilizar la misma moneda")
                    return render_template('comprar.html', form = formulario)
                elif not movimientos:
                    flash ("No tienes {}". format(criptoF))
                    return render_template('comprar.html', form = formulario)

                elif calcular_saldo(criptoF) < float(Qfrom):
                    flash ("No tienes suficientes {}". format(criptoF))
                    return render_template('comprar.html', form = formulario)

                elif type(Qfrom) is not float:
                    flash ("La cantidad introducida debe ser un número")
                    return render_template('comprar.html', form = formulario)
                
                elif Qfrom < 0:
                    flash ("La cantidad introducida no puede ser un número negativo")
                    return render_template('comprar.html', form = formulario)
                
                else:
                
                    url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY=d6a12093-2975-407e-8c90-8b73b5be116a"

                    resultado = requests.get(url.format(Qfrom, criptoF, criptoTo))
                    if resultado.status_code == 200:
                    
                        criptoMonedas = resultado.json()
                            
                        if criptoMonedas ["status"]["error_code"] != 0:
                            flash("Error en la API: " + criptoMonedas["status"]["error_message"])
                            return render_template('comprar.html', form = formulario)
                        
                        
                        cantidadTo = criptoMonedas["data"]["quote"][criptoTo]["price"]
                        formulario.Qto.data = cantidadTo
                        pu = Qfrom / formulario.Qto.data
                        formulario.PU.data = pu
                        
                        return render_template('comprar.html', form = formulario, cantidadTo = cantidadTo, pu=pu)

                    else:
                        flash("Error en el acceso a la API, intentarlo de nuevo más tarde")
                        return render_template('comprar.html', form = formulario)

        else:
            return render_template('inicio.html')
      
               
            
@app.route('/status')
def status():
    inversion = eurosInvertidos('EUR')
    saldoTotal = 0
    
    diccMonedas = {
        'EUR':0, 
        'ETH':0,
        'LTC':0,
        'BNB':0,
        'EOS':0,
        'XLM':0,
        'TRX': 0, 
        'BTC': 0,
        'XRP': 0,
        'BCH':0,
        'USDT':0,
        'BSV':0,
        'ADA':0
    }

    for clave in diccMonedas:
        diccMonedas[clave] = calcular_saldo(clave)

    for key, value in diccMonedas.items():    
        if key != 'EUR' and value != 0:

            cantidad = value
            clave = key
        
            url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY=d6a12093-2975-407e-8c90-8b73b5be116a"

            resultado = requests.get(url.format(cantidad, clave, 'EUR'))
            if resultado.status_code == 200:
                            
                criptoMonedas = resultado.json() 
                saldoCripto = criptoMonedas["data"]["quote"]['EUR']["price"]
                saldoTotal += saldoCripto
    
    saldoEuros = calcular_saldo('EUR')

    valorActual = saldoTotal + saldoEuros + inversion 
   
    return render_template('status.html', inversion=inversion, valorActual=valorActual)

