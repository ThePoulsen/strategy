## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, StringField, SelectField, TextAreaField, SelectMultipleField, validators, SubmitField, DateField, DecimalField
from wtforms.validators import InputRequired, Email, ValidationError
from app.admin.services import  select2MultipleWidget, select2Widget, FlexibleDecimalField



class indicatorForm(FlaskForm):
    indicatorTitle = StringField('Title', [InputRequired('Please enter an indicator title')])
    indicatorDesc = TextAreaField('Description')
    indicatorDataSource = StringField('Data source')
    indicatorMeasurementFrequency = SelectField('Measurement Frequency',validators=[],choices=[],widget=select2Widget())
    indicatorUOM = SelectField('Unit of measure',choices=[],widget=select2Widget())
    indicatorProcessType = SelectField('Process type',choices=[],widget=select2Widget())
    indicatorIndicatorType = SelectField('Indicator type',choices=[],widget=select2Widget())
    indicatorGoodPerformance = SelectField('Good performance',choices=[],widget=select2Widget())
    indicatorOwner = SelectField('Indicator owner', choices=[], widget=select2Widget())
    indicatorResponsible = SelectMultipleField('Indicator Responsible', choices=[], widget=select2MultipleWidget())
    indicatorSubmit = SubmitField('OK')

class selectIndicatorForm(FlaskForm):
    indicator = SelectField('Indicator',validators=[],choices=[],widget=select2Widget())

class newIndicatorTarget(FlaskForm):
    targetValidFrom = DateField('Valid From', format="%d/%m/%Y", validators=[InputRequired('Please select a date')])
    targetValidTo = DateField('Valid To', format="%d/%m/%Y", validators=[InputRequired('Please select a date')])
    valueFrom = FlexibleDecimalField('Value from', validators=[InputRequired('Please enter a value')])
    valueTo = FlexibleDecimalField('Value to')

    def validate_valueTo(self, field):
        if field.data <= self.valueFrom.data:
            raise ValidationError('"Value to" must be higher than "Value from"')
