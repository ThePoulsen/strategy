## -*- coding: utf-8 -*-

from models import measurementFrequency, UOM, processType, indicatorType, goodPerformance
from app.crud.userCRUD import getUsers

def frequencyList():
    data = [(str(r.id),r.title) for r in measurementFrequency.query.all()]
    data.insert(0,('',''))
    return data

def uomList():
    data = [(str(r.id),r.title) for r in UOM.query.all()]
    data.insert(0,('',''))
    return data

def processTypeList():
    data = [(str(r.id),r.title) for r in processType.query.order_by(processType.title.asc()).all()]
    data.insert(0,('',''))
    return data

def indicatorTypeList():
    data = [(str(r.id),r.title) for r in indicatorType.query.order_by(indicatorType.title.asc()).all()]
    data.insert(0,('',''))
    return data

def goodPerformanceList():
    data = [(str(r.id),r.title) for r in goodPerformance.query.order_by(goodPerformance.title.asc()).all()]
    data.insert(0,('',''))
    return data

def userList():
    data = [(str(r['uuid']),r['name']) for r in getUsers()['users']]
    data.insert(0,('',''))
    return data
