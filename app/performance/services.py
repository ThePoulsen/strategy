## -*- coding: utf-8 -*-

from models import indicator
from app.crud.tenantCRUD import getCurrentTenant
from app.crud.userCRUD import getUser
from app.masterData.models import measurementFrequency, UOM, processType, indicatorType, goodPerformance, responsibilityType, responsibilityObject, responsibilityAssignment

def indicatorList():
    indList = [(i.uuid, i.title) for i in indicator.query.filter_by(tenant_uuid=unicode(getCurrentTenant()['uuid'])).all()]
    indList.insert(0,('',''))
    return indList

def indicatorDetails(uuid):
    ind = indicator.query.filter_by(uuid=uuid).first()
    respOwner = responsibilityType.query.filter_by(title='Owner').first()
    resp = responsibilityType.query.filter_by(title='Responsible').first()
    respObj = responsibilityObject.query.filter_by(title='Indicator').first()
    owner_uuid = responsibilityAssignment.query.filter_by(responsibilityObject_id = respObj.id,
                                                          responsibilityType_id = respOwner.id,
                                                          reference_uuid = uuid).first().user_uuid
    try:
        owner = getUser(owner_uuid)['user']
    except:
        owner = {'name':''}


    respIdList = responsibilityAssignment.query.filter_by(responsibilityObject_id = respObj.id,
                                                          responsibilityType_id = resp.id,
                                                          reference_uuid = uuid).all()

    try:
        respList = [getUser(r.user_uuid)['user']['name'] for r in respIdList]
    except:
        respList = []

    try:
        mf = measurementFrequency.query.filter_by(id=ind.measurementFrequency_id).first().title
    except:
        mf = ''

    try:
        uom = UOM.query.filter_by(id=ind.UOM_id).first().title
    except:
        uom = ''

    try:
        pt = processType.query.filter_by(id=ind.processType_id).first().title
    except:
        pt = ''

    try:
        it = indicatorType.query.filter_by(id=ind.indicatorType_id).first().title
    except:
        it = ''

    try:
        gp = goodPerformance.query.filter_by(id=ind.goodPerformance_id).first().title
    except:
        gp = ''

    data = {'title':ind.title,
            'desc':ind.desc,
            'dataSource':ind.dataSource,
            'measurementFrequency':mf,
            'UOM':uom,
            'processType':pt,
            'indicatorType':it,
            'goodPerformance':gp,
            'owner':owner['name'],
            'responsible':respList}

    return data
