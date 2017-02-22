## -*- coding: utf-8 -*-

from flask import session
from authAPI import authAPI

def getGroups(includes=None):
    if includes:
        includeString = '?'
        for r in includes:
            includeString = includeString + unicode(r) + unicode('=True&')
        return authAPI(endpoint='group'+includeString, method='get', token=session['token'])
    else:
        return authAPI(endpoint='group', method='get', token=session['token'])

def postGroup(dataDict):
    return authAPI(endpoint='group', method='post', dataDict=dataDict, token=session['token'])

def putGroup(dataDict, uuid):
    return authAPI(endpoint='group/'+unicode(uuid), method='put', dataDict=dataDict, token=session['token'])

def deleteGroup(uuid):
    return authAPI(endpoint='group/'+unicode(uuid), method='delete', token=session['token'])

def getGroup(uuid, includes=None):
    if includes:
        includeString = '?'
        for r in includes:
            includeString = includeString + unicode(r) + unicode('=True&')
        return authAPI(endpoint='group/'+unicode(uuid)+includeString, method='get', token=session['token'])
    else:
        return authAPI(endpoint='group/'+unicode(uuid), method='get', token=session['token'])

def checkGroup(groupName):
    groups = getGroups()['groups']
    exists = False
    for g in groups:
        if g['name'] == groupName:
            exists = True
    return exists
