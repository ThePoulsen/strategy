## -*- coding: utf-8 -*-

from models import indicator
from app.crud.tenantCRUD import getCurrentTenant

def indicatorList():
    indList = [(i.uuid, i.title) for i in indicator.query.filter_by(tenant_uuid=unicode(getCurrentTenant()['uuid'])).all()]
    indList.insert(0,('',''))
    return indList
