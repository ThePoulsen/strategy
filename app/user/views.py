## -*- coding: utf-8 -*-

from flask import Blueprint, session, render_template, url_for, jsonify, json, g, redirect, request
from app.admin.services import loginRequired, requiredRole, errorMessage, successMessage, apiMessage, sendMail
from forms import changePasswordForm, userForm, groupForm
import requests, flask_sijax
from app.sijax.handler import SijaxHandler
from authAPI import authAPI
from app.crud.groupCRUD import getGroups, postGroup, deleteGroup, getGroup, putGroup
from app.crud.userCRUD import getUsers, getUser, postUser, putUser, deleteUser
from services import usersTable

userBP = Blueprint('userBP', __name__, template_folder='templates')

# User profile
@userBP.route('/profile', methods=['GET'])
@requiredRole('User')
@loginRequired
def userProfileView():
    kwargs = {'title':'User profile'}

    return render_template('user/userProfileView.html', **kwargs)

@userBP.route('/changePassword', methods=['GET','POST'])
@requiredRole('User')
@loginRequired
def changePasswordView():
    kwargs = {'formWidth':300,
              'contentTitle':'Change password'}

    form = changePasswordForm()

    if form.validate_on_submit():
        dataDict = {'password':form.password.data}

        req = authAPI(endpoint='changePassword', method='put', dataDict=dataDict, token=session['token'])
        if 'error' in req:
            if req['error'] == 'Could not identify access token':
                errorMessage(req['error'])

            elif req['error'] == 'Could not identify Platform':
                errorMessage(req['error'])

            elif req['error'] == 'Request data incomplete':
                errorMessage(req['error'])

            elif req['error'] == 'Illegal null values present in request data':
                errorMessage(req['error'])

            elif req['error'] == 'Invalid access token':
                errorMessage(req['error'])

            elif req['error'] == 'Invalid server error':
                errorMessage(req['error'])
            else:
                errorMessage(req['error'])

        else:
            successMessage('Your password has been changed')

    return render_template('user/changePasswordForm.html', form=form, **kwargs)

@flask_sijax.route(userBP, '/user', methods=['GET'])
@flask_sijax.route(userBP, '/user/<string:function>', methods=['GET', 'POST'])
@flask_sijax.route(userBP, '/user/<string:function>/<string:uuid>', methods=['GET', 'POST'])
@requiredRole(u'Administrator')
@loginRequired
def userView(uuid=None, function=None):
    # universal variables
    form = userForm()
    kwargs = {'title':'Users',
              'width':'',
              'formWidth':'400'}

    # Get users
    if function == None:
        kwargs['tableColumns'] =['User name','Email','Roles','Groups']
        kwargs['tableData'] = usersTable()
        return render_template('listView.html', **kwargs)

    elif function == 'delete':
        delUsr = deleteUser(uuid)
        apiMessage(delUsr)

        return redirect(url_for('userBP.userView'))
    else:
        if function == 'update':
            usr = getUser(uuid=uuid, includes=['includeRoles', 'includeGroups'])['user']
            kwargs['contentTitle'] = 'Update user'
            role = 'User'
            for r in usr['roles']:
                if r['title'] == 'Administrator':
                    role = 'Administrator'
                elif r['title'] == 'Superuser':
                    role = 'Superuser'
            grpForm = groupForm()
            usrForm = userForm(userName = usr['name'],
                            userEmail = usr['email'],
                            userPhone = usr['phone'],
                            userGroups = [str(r['uuid']) for r in usr['groups']],
                            userRole = role)

            # Get all groups
            usrForm.userGroups.choices = [(str(r['uuid']),r['name']) for r in getGroups()['groups']]
            if g.sijax.is_sijax_request:
                g.sijax.register_object(SijaxHandler)
                return g.sijax.process_request()

            if usrForm.validate_on_submit():
                dataDict = {'name': usrForm.userName.data,
                            'email': usrForm.userEmail.data,
                            'phone': usrForm.userPhone.data,
                            'roles': [usrForm.userRole.data],
                            'groups': usrForm.userGroups.data}

                updateUser = putUser(dataDict=dataDict, uuid=uuid)
                if not 'error' in updateUser:
                    apiMessage(updateUser)
                    return redirect(url_for('userBP.userView'))
                else:
                    apiMessage(updateUser)

            return render_template('user/userForm.html', usrForm=usrForm, grpForm=grpForm, **kwargs)
        elif function == 'new':
            usrForm = userForm(userRole='User')
            grpForm = groupForm()
            grpForm.groupUsers.choices = [(str(r['uuid']),r['email']) for r in getUsers()['users']]
            kwargs['contentTitle'] = 'New user'
            groups = [(str(r['uuid']),r['name']) for r in getGroups()['groups']]
            usrForm.userGroups.choices = groups

            if g.sijax.is_sijax_request:
                g.sijax.register_object(SijaxHandler)
                return g.sijax.process_request()

            if usrForm.validate_on_submit():
                dataDict = {'name':usrForm.userName.data,
                            'email':usrForm.userEmail.data,
                            'phone':usrForm.userPhone.data}

                roles = ['User']
                if usrForm.userRole.data == 'Superuser':
                    roles.append('Superuser')
                elif usrForm.userRole.data == 'Administrator':
                    roles.append('Superuser')
                    roles.append('Administrator')

                dataDict['roles'] = roles
                dataDict['groups'] = usrForm.userGroups.data
                newUser = postUser(dataDict)
                if 'success' in newUser:
                    successMessage('The user has been created')
                    subject = u'Confirm signup'
                    confirm_url = url_for('authBP.confirmEmailView',token=newUser['token'], _external=True)
                    html = render_template('email/verify.html', confirm_url=confirm_url)

                    sendMail(subject=subject,
                         sender='Henrik Poulsen',
                         recipients=[usrForm.userEmail.data],
                         html_body=html,
                         text_body = None)


                    return redirect(url_for('userBP.userView'))
                else:
                    apiMessage(newUser)
            return render_template('user/userForm.html', usrForm=usrForm, grpForm=grpForm, **kwargs)

    return render_template('listView.html', **kwargs)

# Group View
@userBP.route('/group', methods=['GET'])
@userBP.route('/group/<string:function>', methods=['GET', 'POST'])
@userBP.route('/group/<string:function>/<string:uuid>', methods=['GET', 'POST'])
@loginRequired
@requiredRole(u'Administrator')
def groupView(function=None, uuid=None):
    # global variables
    kwargs = {'title':'User groups',
              'width':'600',
              'formWidth':'350',
              'contentTitle':'Add new user Group',
              'tableColumns':['User group','Description' ,'Users assigned to group']}

    if function == None:
        # perform API request
        req = getGroups(includes=['includeUsers'])['groups']

        # set data for listView
        kwargs['tableData'] = [[r['uuid'],r['name'], r['desc'],len(r['users'])] for r in req]

        # return view
        return render_template('listView.html', **kwargs)
    elif function == 'delete':
        delGroup = deleteGroup(uuid)
        apiMessage(delGroup)

        return redirect(url_for('userBP.groupView'))

    else:
        if function == 'update':
            # Get single group
            grp = getGroup(uuid, includes=['includeUsers'])['group']
            form = groupForm(groupName=grp['name'],
                             groupDesc=grp['desc'],
                             groupUsers = [unicode(r['uuid']) for r in grp['users']])
            form.groupUsers.choices = [(unicode(r['uuid']),r['email']) for r in getUsers()['users']]
            if form.validate_on_submit():
                dataDict = {'name':form.groupName.data,
                            'desc':form.groupDesc.data,
                            'users':[unicode(r) for r in form.groupUsers.data]}
                updateGroup = putGroup(dataDict=dataDict, uuid=uuid)
                if 'error' in updateGroup:
                    apiMessage(updateGroup)
                else:
                    apiMessage(updateGroup)
                    return redirect(url_for('userBP.groupView'))

        elif function == 'new':
            form = groupForm()
            form.groupUsers.choices = [(unicode(r['uuid']),r['email']) for r in getUsers()['users']]

            if form.validate_on_submit():
                dataDict = {'name':form.groupName.data,
                            'desc':form.groupDesc.data,
                            'users':[unicode(r) for r in form.groupUsers.data]}
                newGroup = postGroup(dataDict)
                if 'error' in newGroup:
                    apiMessage(newGroup)
                else:
                    apiMessage(newGroup)
                    return redirect(url_for('userBP.groupView'))
        return render_template('user/groupForm.html', form=form, **kwargs)
