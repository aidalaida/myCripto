from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms.fields.core import BooleanField, SelectField, StringField, FloatField
from wtforms.fields.simple import HiddenField, SubmitField, TextField #clase que se convierte en campo de tipo fecha
from wtforms.validators import DataRequired, Length, ValidationError #clase
from datetime import date

class criptosForm(FlaskForm):
    
    id = HiddenField()
    criptoF = SelectField("criptoF", choices=['','EUR', 'ETH', 'LTC', 'BNB', 'EOS', 'XLM', 'TRX', 'BTC', 'XRP', 'BCH', 'USDT', 'BSV', 'ADA'])
    Qfrom = FloatField("Qfrom", validators = [DataRequired()])
    criptoTo = SelectField("criptoTo", choices=['','EUR', 'ETH', 'LTC', 'BNB', 'EOS', 'XLM', 'TRX', 'BTC', 'XRP', 'BCH', 'USDT', 'BSV', 'ADA'])
    Qto = FloatField("Qto")
    PU = FloatField("P.U.")
    submit = SubmitField("Filtrar")
    
    