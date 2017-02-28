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
    owner = getUser(owner_uuid)['user']
    respList = responsibilityAssignment.query.filter_by(responsibilityObject_id = respObj.id,
                                                          responsibilityType_id = resp.id,
                                                          reference_uuid = uuid).all()


    data = {'title':ind.title, 'desc':ind.desc,'dataSource':ind.dataSource, 'measurementFrequency':measurementFrequency.query.filter_by(id=ind.measurementFrequency_id).first().title,
           'UOM':UOM.query.filter_by(id=ind.UOM_id).first().title,
           'processType':processType.query.filter_by(id=ind.processType_id).first().title,
           'indicatorType':indicatorType.query.filter_by(id=ind.indicatorType_id).first().title,
           'goodPerformance':goodPerformance.query.filter_by(id=ind.goodPerformance_id).first().title,
           'owner':owner['name'],
           'responsible':[getUser(r.user_uuid)['user']['name'] for r in respList]}
    return data
