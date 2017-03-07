## -*- coding: utf-8 -*-

from app import db

class chartContainer(db.Model):
    __tablename__ = 'chartContainer'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())

    chartType_id = db.Column(db.Integer, db.ForeignKey('chartType.id'))
    containerSize_id = db.Column(db.Integer, db.ForeignKey('containerSize.id'))
    indicator_id = db.Column(db.Integer, db.ForeignKey('indicator.id'))

    tenant_uuid = db.Column(db.String())
    user_uuid = db.Column(db.String())
