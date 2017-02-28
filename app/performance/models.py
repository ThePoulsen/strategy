## -*- coding: utf-8 -*-

from app import db
from datetime import datetime

class indicator(db.Model):
    __tablename__ = 'indicator'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), unique=True)
    title = db.Column(db.String(), unique=True)
    desc = db.Column(db.String())
    dataSource = db.Column(db.String())

    tenant_uuid = db.Column(db.String())

    measurementFrequency_id = db.Column(db.Integer, db.ForeignKey('measurementFrequency.id'))
    UOM_id = db.Column(db.Integer, db.ForeignKey('UOM.id'))
    processType_id = db.Column(db.Integer, db.ForeignKey('processType.id'))
    indicatorType_id = db.Column(db.Integer, db.ForeignKey('indicatorType.id'))
    goodPerformance_id = db.Column(db.Integer, db.ForeignKey('goodPerformance.id'))

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
