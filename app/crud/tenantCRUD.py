## -*- coding: utf-8 -*-

from flask import session, json
from authAPI import authAPI

def getCurrentTenant():
    tok = session['token']
    tenant = authAPI(endpoint='returnCurrentTenant', method='post', token=session['token'])
    if 'success' in tenant:
        tenant_uuid = tenant['success']
        return authAPI(endpoint='tenant/'+unicode(tenant_uuid), method='get', token=session['token'])['tenant']
    else:
        return False

def putTenant(uuid, dataDict):
    return authAPI(endpoint='tenant/'+unicode(uuid), method='put', token=session['token'], dataDict=dataDict)
