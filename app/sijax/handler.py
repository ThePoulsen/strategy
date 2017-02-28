## -*- coding: utf-8 -*-
import json
from services import sijaxSuccess
from app.performance.models import indicator, indicatorTarget
from app.crud.groupCRUD import postGroup, checkGroup
from app.crud.userCRUD import getUser

class SijaxHandler(object):
    """A container class for all Sijax handlers.
    Grouping all Sijax handler functions in a class
    (or a Python module) allows them all to be registered with
    a single line of code.
    """

    @staticmethod
    def getContactDetails(obj_response, uuid):
        usr = getUser(uuid)['user']
        obj_response.attr('#email', 'value', usr['email'])
        obj_response.attr('#phone', 'value', usr['phone'])

    @staticmethod
    def getIndicator(obj_response, uuid):
#        usr = indicatorTarget.
        obj_response.attr('#currentTarget', 'value', usr['email'])
        obj_response.attr('#currentValidFrom', 'value', usr['phone'])
        obj_response.attr('#currentValidTo', 'value', usr['phone'])

    @staticmethod
    def userFormGroupModal(obj_response, values):
        required=['groupName','groupDesc']

        groupName = values['groupName']
        groupDesc = values['groupDesc']

        dataDict = {'name':groupName,
                    'desc':groupDesc,
                    'users':[]}

        validations = []
        grpExists = checkGroup(groupName)

        if groupName == '':
            validations.append(('groupName','Input Required'))
        if groupDesc == '':
            validations.append(('groupDesc','Input Required'))

        if len(validations) > 0:
            for r in required:
                obj_response.html('#'+r+'Validator', '')
            for r in validations:
                obj_response.html('#'+r[0]+'Validator', r[1])

        elif grpExists:
            obj_response.html('#groupNameValidator', sijaxSuccess('The group already exist'))

        else:
            grp = postGroup(dataDict)
            if 'success' in grp:
                groupID = grp['uuid']
                for r in required:
                    obj_response.html('#'+r+'Validator', '')
                obj_response.script("$('#newGroupFrom')[0].reset();")
                obj_response.script("$('#newGroupModal').modal('hide')")
                obj_response.script("$('#userGroups').append($('<option></option>').attr('value', '{}').attr('selected', 'true').text('{}'));".format(groupID,groupName))
                obj_response.html('#flashDiv', sijaxSuccess('The group has been added'))
            else:
                obj_response.html('#flashDiv', sijaxSuccess('The group has been added'))
