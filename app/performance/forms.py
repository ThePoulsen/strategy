## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField, BooleanField, SelectMultipleField, RadioField, validators, SubmitField
from wtforms.validators import InputRequired, Email
from app.admin.services import  select2MultipleWidget, select2Widget
from app.masterData.models import measurementFrequency, UOM

class indicatorForm(FlaskForm):

    freq = [(r.id,r.title) for r in measurementFrequency.query.all()]
    freq.insert(0,('',''))

    uomList = [(r.id,r.title) for r in UOM.query.all()]
    uomList.insert(0,('',''))


    indicatorTitle = StringField('Title', validators=[InputRequired('Please enter an indicator title')])
    indicatorDesc = TextAreaField('Description')
    indicatorDataSource = StringField('Data source')

    indicatorMeasurementFrequency = SelectField('Measurement Frequency', validators=[], choices=freq, widget=select2Widget())
    indicatorUOM = SelectField('Unit of measure', choices=uomList, widget=select2Widget())

    indicatorSubmit = SubmitField('OK')
