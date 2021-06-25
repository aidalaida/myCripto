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
                
                query = "INSERT INTO myCRYPTO (fecha, hora, criptoF, Qfrom, criptoTo, Qto) VALUES (?, ?, ?, ?, ?,?)"
                try:
                    fecha = datetime.now().strftime('%Y-%m-%d')
                    hora = datetime.now().strftime('%H:%M:%S')
                    Qto = formulario.Qto.data

                    dbManager.modificaTablaSQL(query, [fecha, hora, formulario.criptoF.data, formulario.Qfrom.data, formulario.criptoTo.data, Qto])
                    
            
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

            url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY=d6a12093-2975-407e-8c90-8b73b5be116a"

            resultado = requests.get(url.format(Qfrom, criptoF, criptoTo))
            if resultado.status_code != 200:
                flash("Error en el acceso a la API, intentarlo de nuevo más tarde")
                return render_template('comprar.html', form = formulario)
            
            criptoMonedas = resultado.json()
                
            if criptoMonedas ["status"]["error_code"] != 0:
                flash("Error en la API: " + criptoMonedas["status"]["error_message"])
                return render_template('comprar.html', form = formulario)
            
            cantidadTo = criptoMonedas["data"]["quote"][criptoTo]["price"]

            formulario.Qto.data = cantidadTo
            formulario.PU.data = Qfrom/cantidadTo
            return render_template('comprar.html', form = formulario)
        else:
            return render_template('inicio.html')
      
               
            


@app.route('/status')
def status():
    return render_template('status.html')

