from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms.fields.core import BooleanField, DecimalField, SelectField, StringField, FloatField
from wtforms.fields.simple import HiddenField, SubmitField, TextAreaField, TextField 
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from datetime import date

from wtforms.widgets.core import TextInput

def funcion_de_errores(formulario, campo):
    if campo.data == formulario.criptoF.data:
        raise ValidationError ("No se puede utilizar la misma moneda")

class criptosForm(FlaskForm):

    criptoF = SelectField("criptoF", choices=['','EUR', 'ETH', 'LTC', 'BNB', 'EOS', 'XLM', 'TRX', 'BTC', 'XRP', 'BCH', 'USDT', 'BSV', 'ADA'], validators = [DataRequired()])
    Qfrom = FloatField("Qfrom", validators = [DataRequired()])
    criptoTo = SelectField("criptoTo", choices=['','EUR', 'ETH', 'LTC', 'BNB', 'EOS', 'XLM', 'TRX', 'BTC', 'XRP', 'BCH', 'USDT', 'BSV', 'ADA'], validators = [DataRequired(), funcion_de_errores])
    Qto = FloatField("CriptoQTo")
    PU = FloatField("Precio unitario")
    calcular = SubmitField("Calcular")
    submit = SubmitField("Aceptar")
    cancelar = SubmitField("Cancelar")
    
    