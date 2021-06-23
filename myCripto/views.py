from flask_wtf import form
from myCripto import app
from flask import jsonify, render_template, request, redirect, url_for, flash
from myCripto import forms
from myCripto.forms import criptosForm
from datetime import date
from datetime import datetime
from myCripto.dataaccess import *
import requests

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
        if formulario.validate:
            query = "INSERT INTO myCRYPTO (fecha, hora, criptoF, Qfrom, criptoTo) VALUES (?, ?, ?, ?, ?)"
            try:
                fecha = datetime.now().strftime('%Y-%m-%d')
                hora = datetime.now().strftime('%H:%M:%S')

                dbManager.modificaTablaSQL(query, [fecha, hora, formulario.criptoF.data, formulario.Qfrom.data, formulario.criptoTo.data])
                
        
            except sqlite3.Error as el_error:
                print("Error en SQL INSERT", el_error)
                flash("Se ha producido un error en la base de datos. Pruebe en unos minutos", "error")
                return render_template('inicio.html', form=formulario)

            return redirect(url_for("index"))
        else:
            return render_template('comprar.html', form = formulario)
       



def llamaApi(formulario):

    print("llama apii")

    criptoF = formulario.criptoF.data
    Qfrom = formulario.Qfrom.data
    criptoTo = formulario.criptoTo.data

    url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY=d6a12093-2975-407e-8c90-8b73b5be116a"

    resultado = request.get(url.format(Qfrom, criptoF, criptoTo))
    if resultado.status_code == 200:
        critpoMonedas = resultado.json()
        if critpoMonedas ['Response'] == "False":
            return jsonify({'status': "Error", "msg": "No se han encontrado resultados"})
        
        print(critpoMonedas["data"])
        return jsonify({"Qto": critpoMonedas["data"], 'status': "Succcess"})

    

@app.route('/status')
def status():
    return render_template('status.html')

