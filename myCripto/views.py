from myCripto import app
from flask import render_template


@app.route('/')
def listaMovimientos():
    return render_template('inicio.html')

@app.route('/compra')
def comprar():
    return render_template('comprar.html')

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')