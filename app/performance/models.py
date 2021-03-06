## -*- coding: utf-8 -*-

from app import db
from datetime import datetime

indicatorChartType = db.Table('indicatorChartType',
    db.Column('chartType_id', db.Integer, db.ForeignKey('chartType.id')),
    db.Column('indicator_id', db.Integer, db.ForeignKey('indicator.id')))

class indicator(db.Model):
    __tablename__ = 'indicator'
    __table_args__ = (db.UniqueConstraint('title', 'tenant_uuid', name='_title_tenant'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), unique=True)
    title = db.Column(db.String())
    desc = db.Column(db.String())
    dataSource = db.Column(db.String())

    tenant_uuid = db.Column(db.String())

    measurementFrequency_id = db.Column(db.Integer, db.ForeignKey('measurementFrequency.id'))
    UOM_id = db.Column(db.Integer, db.ForeignKey('UOM.id'))
    processType_id = db.Column(db.Integer, db.ForeignKey('processType.id'))
    indicatorType_id = db.Column(db.Integer, db.ForeignKey('indicatorType.id'))
    goodPerformance_id = db.Column(db.Integer, db.ForeignKey('goodPerformance.id'))
    
    targets = db.relationship('indicatorTarget', backref='indicator', lazy='dynamic')

    chartTypes = db.relationship('chartType', secondary=indicatorChartType,
        backref=db.backref('indicators', lazy='dynamic'))

class indicatorTarget(db.Model):
    __tablename__ = 'indicatorTarget'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), unique=True)

    fromTarget = db.Column(db.Float)
    toTarget = db.Column(db.Float)

    tenant_uuid = db.Column(db.String())
    indicator_uuid = db.Column(db.String, db.ForeignKey('indicator.uuid'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    validFrom = db.Column(db.Integer, db.ForeignKey('calendar.id'))
    validTo = db.Column(db.Integer, db.ForeignKey('calendar.id'))
