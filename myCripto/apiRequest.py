import requests
from flask import jsonify, render_template, request, redirect, url_for, flash

def consultaAPIFormulario(Qfrom, criptoF, criptoTo, formulario):
    url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY=d6a12093-2975-407e-8c90-8b73b5be116a"

    resultado = requests.get(url.format(Qfrom, criptoF, criptoTo))
    if resultado.status_code == 200:
        criptoMonedas = resultado.json()
                            
        if criptoMonedas ["status"]["error_code"] != 0:
            flash("Error en la API: " + criptoMonedas["status"]["error_message"])
            return render_template('comprar.html', form = formulario)
                                     
    cantidadTo = criptoMonedas["data"]["quote"][criptoTo]["price"]

    return cantidadTo
    

def consultaAPIstatus(cantidad, clave, moneda):
    url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY=d6a12093-2975-407e-8c90-8b73b5be116a"

    resultado = requests.get(url.format(cantidad, clave, 'EUR'))
    if resultado.status_code == 200:
                            
        criptoMonedas = resultado.json()
        saldoCripto = criptoMonedas["data"]["quote"]['EUR']["price"]
    
    return saldoCripto