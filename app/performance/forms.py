## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField, BooleanField, SelectMultipleField, RadioField, validators, SubmitField
from wtforms.validators import InputRequired, Email
from app.admin.services import  select2MultipleWidget, select2Widget


class indicatorForm(FlaskForm):

    indicatorTitle = StringField('Title', validators=[InputRequired('Please enter an indicator title')])
    indicatorDesc = TextAreaField('Description')
    indicatorDataSource = StringField('Data source')

    indicatorMeasurementFrequency = SelectField('Measurement Frequency', validators=[], choices=[], widget=select2Widget())
    indicatorUOM = SelectField('Unit of measure', choices=[], widget=select2Widget())
    indicatorProcessType = SelectField('Process type', choices=[], widget=select2Widget())
    indicatorIndicatorType = SelectField('Indicator type', choices=[], widget=select2Widget())
    indicatorGoodPerformance = SelectField('Good performance', choices=[], widget=select2Widget())

    indicatorOwner = SelectField('Indicator owner', choices=[], widget=select2Widget())
    indicatorResponsible = SelectMultipleField('Indicator Responsible', choices=[], widget=select2MultipleWidget())

    indicatorSubmit = SubmitField('OK')
