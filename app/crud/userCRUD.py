## -*- coding: utf-8 -*-

from flask import session, json
from authAPI import authAPI

def getUsers(includes=None):
    if includes:
        includeString = '?'
        for r in includes:
            includeString = includeString + unicode(r) + unicode('=True&')
        return authAPI(endpoint='user'+includeString, method='get', token=session['token'])
    else:
        return authAPI(endpoint='user', method='get', token=session['token'])

def getUser(uuid, includes=None):
    if includes:
        includeString = '?'
        for r in includes:
            includeString = includeString + unicode(r) + unicode('=True&')
        return authAPI(endpoint='user/'+unicode(uuid)+includeString, method='get', token=session['token'])
    else:
        return authAPI(endpoint='user/'+unicode(uuid), method='get', token=session['token'])

def postUser(dataDict):
    req = authAPI(endpoint='user', method='post', dataDict=dataDict, token=session['token'])
    print req
    if 'success' in req:
        return req
    else:
        if req['error'] == 'Could not identify access token':
            return {'error':req['error']}

        elif req['error'] == 'Could not identify Platform':
            return {'error':req['error']}

        elif req['error'] == 'You are not authorized to view this content':
            return {'error':req['error']}

        elif req['error'] == 'User already exist':
            return {'error':req['error']}

        elif req['error'] == 'Not valid email-address':
            return {'error':req['error']}

        elif req['error'] == 'Internal server error':
            return {'error':req['error']}

        elif req['error'] == 'Invalid access token':
            return {'error':req['error']}

def putUser(dataDict, uuid):
    return authAPI(endpoint='user/'+unicode(uuid), method='put', dataDict=dataDict, token=session['token'])

def deleteUser(uuid):
    return authAPI(endpoint='user/'+unicode(uuid), method='delete', token=session['token'])

def getContactPerson():
    return authAPI(endpoint='contactPerson', method='post', token=session['token'])

def removeContactPerson(uuid):
    return authAPI(endpoint='removeContact/'+unicode(uuid), method='post', token=session['token'])

def addContactPerson(uuid):
    return authAPI(endpoint='addContact/'+unicode(uuid), method='post', token=session['token'])
