from flask_wtf import form
from myCripto import app
from flask import jsonify, render_template, request, redirect, url_for, flash
from myCripto import forms
from myCripto.forms import criptosForm
import sqlite3


@app.route('/')
def index():
   return render_template('inicio.html')

@app.route('/inicio')
def inicio():
    conexion = sqlite3.connect("movimientosCripto.db")
    cur = conexion.cursor()

    cur.execute("SELECT * From myCRYPTO;")
    
    claves = cur.description
    filas = cur.fetchall()
    
    movimientos = []
    for fila in filas:
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]]= valor
        movimientos.append(d)

    conexion.close()

    return render_template('inicio.html', datos = movimientos)


@app.route('/purchase', methods=['GET', 'POST'])
def comprar():
    print("ha entrado")
    formulario = criptosForm()
    if request.method == 'GET':
        print("ha entrado GET")
        return render_template('comprar.html', form = formulario)
    else:
        print(formulario.Qto)
        if formulario.validate():
            query = "INSERT INTO myCRYPTO (criptoF, Qfrom, criptoTo, Qto) VALUES (?, ?, ?, ?)"
            print("fdgviufwabifbuoabo")

            conexion = sqlite3.connect("movimientosCripto.db")
            cur = conexion.cursor()

            cur.execute(query, [formulario.criptoF.data, formulario.Qfrom.data, formulario.criptoTo.data, formulario.Qto.data])
            conexion.commit()
            conexion.close()

            return redirect(url_for("inicio"))
        else:
            return render_template('comprar.html', form = formulario)

@app.route('/', methods=['GET', 'POST'])    
def calcular(Qfrom, From, To):
    url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY=d6a12093-2975-407e-8c90-8b73b5be116a"

    resultado = request.get(url.format(Qfrom, From, To))
    if resultado.status_code == 200:
        Qto = resultado.json()
        print()







@app.route('/status')
def status():
    return render_template('status.html')

