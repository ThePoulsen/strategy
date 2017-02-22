## -*- coding: utf-8 -*-

from app import db

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
