## -*- coding: utf-8 -*-
## project/app/admin/views.py

from app import db
from flask import Blueprint, render_template, request, redirect, url_for, session, g
from app.admin.services import requiredRole, loginRequired, errorMessage, successMessage
from models import indicator
from app.crud.tenantCRUD import getCurrentTenant
from app.crud.userCRUD import getUsers
from forms import indicatorForm
from app.masterData.models import measurementFrequency, UOM, processType, indicatorType, goodPerformance

perfBP = Blueprint('perfBP', __name__, template_folder='templates')

@perfBP.route('/indicator', methods=['GET'])
@loginRequired
@requiredRole([u'User', u'Superuser', u'Administrator'])
def indicatorListView(function=None, uuid=None):
    kwargs = {'title':'Performance indicators',
              'contentTitle':'Add new performance indicator',
              'tableColumns':['Indicator','Description' ,'Target', 'Actual', 'Deviation', 'Development']}

    tenant = getCurrentTenant()
    if tenant:
        if function == None:
            # perform API request
            indicators = indicator.query.filter_by(tenant_uuid = tenant['uuid'])

            # set data for listView
            kwargs['tableData'] = [[r['uuid'],r['title'], r['desc'],'','','',''] for r in indicators]

            # return view
            return render_template('listView.html', **kwargs)

    else:
        errorMessage('Cannot verify your account, please log in again')
        return redirect(url_for('indexView'))

@perfBP.route('/indicator/details/<string:uuid>', methods=['GET'])
@loginRequired
@requiredRole([u'User', u'Superuser', u'Administrator'])
def indicatorDetailsView(uuid=None):
    pass

@perfBP.route('/indicator/<string:function>/', methods=['GET', 'POST'])
@perfBP.route('/indicator/modify/<string:uuid>', methods=['GET', 'POST'])
@perfBP.route('/indicator/delete/<string:uuid>', methods=['GET', 'POST'])
@loginRequired
@requiredRole([u'Superuser', u'Administrator'])
def indicatorManagementView(uuid=None, function=None):
    kwargs = {}
    # measurement frequencies
    freq = [(r.id,r.title) for r in measurementFrequency.query.all()]
    freq.insert(0,('',''))
    # Units of measure
    uomList = [(r.id,r.title) for r in UOM.query.order_by(UOM.title.asc()).all()]
    uomList.insert(0,('',''))
    # Units of measure
    pt = [(r.id,r.title) for r in processType.query.order_by(processType.title.asc()).all()]
    pt.insert(0,('',''))
    # Units of measure
    it = [(r.id,r.title) for r in indicatorType.query.order_by(indicatorType.title.asc()).all()]
    it.insert(0,('',''))
    # Units of measure
    gp = [(r.id,r.title) for r in goodPerformance.query.order_by(goodPerformance.title.asc()).all()]
    gp.insert(0,('',''))
    # owner/resp
    usrList = [(r['uuid'],r['name']) for r in getUsers()['users']]
    usrList.insert(0,('',''))


    # functions
    if function == 'new' and uuid == None:
        indicatorFrm = indicatorForm()
        indicatorFrm.indicatorMeasurementFrequency.choices = freq
        indicatorFrm.indicatorUOM.choices = uomList
        indicatorFrm.indicatorProcessType.choices = pt
        indicatorFrm.indicatorIndicatorType.choices = it
        indicatorFrm.indicatorGoodPerformance.choices = gp
        indicatorFrm.indicatorOwner.choices = usrList
        indicatorFrm.indicatorResponsible.choices = usrList


        kwargs['contentTitle'] = 'Create new Performance Indicator'
        return render_template('performance/indicatorForm.html', indicatorForm=indicatorFrm, **kwargs)
