from os import putenv
from flask_wtf import form
from myCripto import app
from flask import jsonify, render_template, request, redirect, url_for, flash
from myCripto import forms
import myCripto
from myCripto.forms import criptosForm
from datetime import date
from datetime import datetime
from myCripto.dataaccess import *
import requests
import json
from myCripto.balances import *
from myCripto.apiRequest import *
from myCripto.validations import *

dbManager = DBmanager()

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
                            
                elif validationFormulario(criptoF, criptoTo, Qfrom, formulario):
                    return render_template('comprar.html', form = formulario)
                
                else:
                    cantidadTo = consultaAPIFormulario(Qfrom, criptoF, criptoTo, formulario)
                    
                    formulario.Qto.data = cantidadTo
                    pu = Qfrom / formulario.Qto.data
                    formulario.PU.data = pu
                            
                    return render_template('comprar.html', form = formulario, cantidadTo = cantidadTo, pu=pu)

                  
            else:
                query = "SELECT * From myCRYPTO WHERE criptoTo=?;"
                parametros = [criptoF]
                movimientos = dbManager.consultaSQL(query, parametros)

                if not movimientos:
                    flash ("No tienes {}". format(criptoF))
                    return render_template('comprar.html', form = formulario)

                elif validationFormulario(criptoF, criptoTo, Qfrom, formulario):
                    return render_template('comprar.html', form = formulario)

                elif calcular_saldo(criptoF) < float(Qfrom):
                    flash ("No tienes suficientes {}". format(criptoF))
                    return render_template('comprar.html', form = formulario)
                
                else:
                    cantidadTo = consultaAPIFormulario(Qfrom, criptoF, criptoTo)
                    formulario.Qto.data = cantidadTo
                    pu = Qfrom / formulario.Qto.data
                    formulario.PU.data = pu
                        
                    return render_template('comprar.html', form = formulario, cantidadTo = cantidadTo, pu=pu)
        else:
            return render_template('inicio.html')
      
               
            
@app.route('/status')
def status():
    inversion = eurosInvertidos('EUR')
    saldoTotal = 0
    
    diccMonedas = {'EUR':0, 'ETH':0,'LTC':0, 'BNB':0, 'EOS':0, 'XLM':0, 'TRX': 0,  'BTC': 0, 'XRP': 0, 'BCH':0, 'USDT':0, 'BSV':0, 'ADA':0
    }

    for clave in diccMonedas:
        diccMonedas[clave] = calcular_saldo(clave)

    for key, value in diccMonedas.items():    
        if key != 'EUR' and value != 0:

            cantidad = value
            clave = key

            saldoCripto = consultaAPIstatus(cantidad, clave, 'EUR')
            saldoTotal += saldoCripto
    
    saldoEuros = calcular_saldo('EUR')

    valorActual = saldoTotal + saldoEuros + inversion 
   
    return render_template('status.html', inversion=inversion, valorActual=valorActual)

