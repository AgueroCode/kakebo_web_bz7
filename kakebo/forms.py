from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms.fields.core import BooleanField, FloatField, SelectField, StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length

class MovimientosForm(FlaskForm):
    fecha = DateField("Fecha", validators=[DataRequired()])
    concepto = StringField("Concepto", validators=[DataRequired(), Length(min=10)])
    categoria = SelectField("Categoria", choices=[('SU', 'Supervivencia'), ('OV', 'Ocio/Vicio'),
                            ('CU', 'Cultura'), ('EX', 'Extras')])
    cantidad = FloatField("Cantidad", validators=[DataRequired()])
    esGasto = BooleanField("Es gasto")
    submit = SubmitField("Aceptar")