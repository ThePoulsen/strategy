## -*- coding: utf-8 -*-

from app import db

class dash(db.Model):
    __tablename__ = 'dash'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())

    tenant_uuid = db.Column(db.String())
    user_uuid = db.Column(db.String())

class dashContainer(db.Model):
    __tablename__ = 'dashContainer'

    id = db.Column(db.Integer, primary_key=True)
    tenant_uuid = db.Column(db.String())

    sequence = db.Column(db.Integer())

    chartContainer_id = db.Column(db.Integer, db.ForeignKey('chartContainer.id'))
    dash_id = db.Column(db.Integer, db.ForeignKey('dash.id'))
