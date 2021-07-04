from flask import jsonify, render_template, request, redirect, url_for, flash

def validationFormulario (criptoF, criptoTo, Qfrom, formulario):
    if criptoF == criptoTo:
        flash ("No se puede utilizar la misma moneda")
        return render_template('comprar.html', form = formulario)
    elif type(Qfrom) is not float:
        flash ("La cantidad introducida debe ser un número. Recuerda que los decimales hay que escribirlos con punto")
        return render_template('comprar.html', form = formulario)
                
    elif Qfrom <= 0:
        flash ("La cantidad introducida tiene que ser mayor que cero")
        return render_template('comprar.html', form = formulario)