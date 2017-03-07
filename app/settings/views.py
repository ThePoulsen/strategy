## -*- coding: utf-8 -*-

from flask import Blueprint, render_template, url_for, g, request, redirect, session, json
from app.admin.services import requiredRole, loginRequired, errorMessage, successMessage
from app import db
from forms import companyForm
from authAPI import authAPI
from app.crud.tenantCRUD import getCurrentTenant, putTenant
from app.crud.userCRUD import getUsers, getContactPerson, removeContactPerson, addContactPerson
from app.sijax.handler import SijaxHandler
import flask_sijax, sys

settingsBP = Blueprint('settingsBP', __name__, template_folder='templates')

@flask_sijax.route(settingsBP, '/company')
@requiredRole([u'Administrator'])
@loginRequired
def companyView():

    kwargs = {'title':'Company information',
              'formWidth':'350'}
    form = companyForm()

    if g.sijax.is_sijax_request:
        g.sijax.register_object(SijaxHandler)
        return g.sijax.process_request()

    tenant = getCurrentTenant()
    contact = getContactPerson()
    if 'error' in contact:
        contact = {'uuid':'',
                   'contactName':None,
                   'email':None,
                   'phone':None}
        errorMessage('Please assign contact person')
    else:
        contact=contact['success']

    form = companyForm(regNo=tenant[u'regNo'],
                       companyName=tenant[u'name'],
                       addr=tenant[u'addr'],
                       addr2=tenant[u'addr2'],
                       postcode=tenant[u'postcode'],
                       city=tenant[u'city'],
                       contactName = str(contact['uuid']),
                       phone=contact['phone'],
                       email=contact['email'])

    users = [(str(r['uuid']),str(r['name']+' - '+r['email'])) for r in getUsers()['users']]
    users.insert(0,('',''))
    form.contactName.choices = users

    if form.validate_on_submit() and request.method == 'POST':
        companyData = {'regNo' : form.regNo.data,
                       'name': form.companyName.data,
                       'addr': form.addr.data,
                       'addr2': form.addr2.data,
                       'postcode':form.postcode.data,
                       'city': form.city.data}


        if not contact['uuid'] == '':
            remCont = removeContactPerson(contact['uuid'])
        addCont = addContactPerson(form.contactName.data)
        if not 'error' in addCont:
            putCont = putTenant(uuid=tenant['uuid'], dataDict=companyData)
            if not 'error' in putCont:
                successMessage('Your company information has been updated')
            else:
                errorMessage(putCont['error'])
        else:
            errorMessage(addCont['error'])



    return render_template('settings/companyView.html', form=form, **kwargs)


@settingsBP.route('/settings')
@requiredRole([u'Administrator'])
@loginRequired
def settingsView():
    kwargs = {'title':'Settings',
              'formWidth':'350'}
    return render_template('settings/settingsView.html', **kwargs)
