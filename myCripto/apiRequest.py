import requests
from myCripto import app
from flask import jsonify, render_template, request, redirect, url_for, flash

api_key = app.config.get('API_KEY')

def consultaAPIFormulario(Qfrom, criptoF, criptoTo, formulario):
    url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"

    resultado = requests.get(url.format(Qfrom, criptoF, criptoTo, api_key))
    if resultado.status_code == 200:
        criptoMonedas = resultado.json()
                            
        if criptoMonedas ["status"]["error_code"] != 0:
            flash("Error en la API: " + criptoMonedas["status"]["error_message"])
            return render_template('comprar.html', form = formulario)
                                     
    cantidadTo = criptoMonedas["data"]["quote"][criptoTo]["price"]

    return cantidadTo
    

def consultaAPIstatus(cantidad, clave, moneda):
    url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"

    resultado = requests.get(url.format(cantidad, clave, 'EUR', api_key))
    if resultado.status_code == 200:
                            
        criptoMonedas = resultado.json()
        saldoCripto = criptoMonedas["data"]["quote"]['EUR']["price"]
    
    return saldoCripto