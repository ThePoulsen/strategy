## -*- coding: utf-8 -*-

from app import db
from flask import Blueprint, render_template, request, redirect, url_for, session, g
from app.admin.services import requiredRole, loginRequired, errorMessage, successMessage, getRoles
from models import indicator
from app.crud.tenantCRUD import getCurrentTenant
from forms import indicatorForm, selectIndicatorForm, newIndicatorTarget
from app.masterData.services import frequencyList, uomList, processTypeList, indicatorTypeList, goodPerformanceList, userList
from services import indicatorList
from app.masterData.models import responsibilityType, responsibilityObject, responsibilityAssignment
import uuid as UUID
import flask_sijax

perfBP = Blueprint('perfBP', __name__, template_folder='templates')

@perfBP.route('/indicator', methods=['GET'])
@loginRequired
@requiredRole([u'User', u'Superuser', u'Administrator'])
def indicatorListView(function=None, uuid=None):
    kwargs = {'title':'Performance indicators',
              'contentTitle':'Current performance indicators',
              'tableColumns':['Indicator','Description' ,'Target', 'Actual', 'Deviation', 'Development']}

    editRoles = [u'Superuser', 'Administrator']


    if not any(i in editRoles for i in getRoles()):
        kwargs['detailsButton'] = True
        kwargs['withoutDeleteEntry'] = True
        kwargs['withoutNewEntry'] = True

    ten = getCurrentTenant()
    if ten:
        if function == None:
            # perform API request
            indicators = indicator.query.filter_by(tenant_uuid = ten['uuid']).all()

            # set data for listView
            kwargs['tableData'] = [[r.uuid,r.title, r.desc,'','','',''] for r in indicators]

            # return view
            return render_template('listView.html', **kwargs)

    else:
        errorMessage('Cannot verify your account, please log in again')
        return redirect(url_for('indexView'))

@perfBP.route('/indicator/details/<string:uuid>', methods=['GET'])
@loginRequired
@requiredRole([u'User', u'Superuser', u'Administrator'])
def indicatorDetailsView(uuid=None):
    ten = getCurrentTenant()
    respTypeOwner = responsibilityType.query.filter_by(title='Owner').first()
    respTypeResponsible = responsibilityType.query.filter_by(title='Responsible').first()
    respObj = responsibilityObject.query.filter_by(title='Indicator').first()
    kwargs = {'contentTitle': 'Indicator details'}
    if ten:

        indFrm = indicatorForm()
        ind = indicator.query.filter_by(uuid=uuid, tenant_uuid=unicode(ten['uuid'])).first()

        owner = responsibilityAssignment.query.filter_by(responsibilityObject_id = respObj.id,
                                                    reference_uuid = unicode(ind.uuid),
                                                    responsibilityType_id = respTypeOwner.id).first()

        resp = responsibilityAssignment.query.filter_by(responsibilityObject_id = respObj.id,
                                                    reference_uuid = unicode(ind.uuid),
                                                    responsibilityType_id = respTypeResponsible.id).all()

        indFrm = indicatorForm(indicatorTitle = ind.title,
                               indicatorDesc = ind.desc,
                               indicatorDataSource = ind.dataSource,
                               indicatorMeasurementFrequency = ind.measurementFrequency_id,
                               indicatorUOM = ind.UOM_id,
                               indicatorProcessType = ind.processType_id,
                               indicatorIndicatorType = ind.indicatorType_id,
                               indicatorGoodPerformance = ind.goodPerformance_id,
                               indicatorOwner = owner.user_uuid if owner else None,
                               indicatorResponsible = [r.user_uuid for r in resp] if resp else None)
        indFrm.indicatorMeasurementFrequency.choices = frequencyList()
        indFrm.indicatorUOM.choices = uomList()
        indFrm.indicatorProcessType.choices = processTypeList()
        indFrm.indicatorIndicatorType.choices = indicatorTypeList()
        indFrm.indicatorGoodPerformance.choices = goodPerformanceList()
        indFrm.indicatorOwner.choices = userList()
        indFrm.indicatorResponsible.choices = userList()

        return render_template('performance/indicatorDetails.html', indicatorForm=indFrm, **kwargs)

    else:
        errorMessage('Cannot verify your account, please log in again')
        return redirect(url_for('indexView'))

@perfBP.route('/indicator/<string:function>/', methods=['GET', 'POST'])
@perfBP.route('/indicator/<string:function>/<string:uuid>', methods=['GET', 'POST'])
@perfBP.route('/indicator/<string:function>/<string:uuid>', methods=['GET', 'POST'])
@loginRequired
@requiredRole([u'Superuser', u'Administrator'])
def indicatorManagementView(uuid=None, function=None):
    kwargs = {}
    ten = getCurrentTenant()
    respTypeOwner = responsibilityType.query.filter_by(title='Owner').first()
    respTypeResponsible = responsibilityType.query.filter_by(title='Responsible').first()
    respObj = responsibilityObject.query.filter_by(title='Indicator').first()

    if ten:
        if function == 'new' and uuid == None:
            kwargs['contentTitle'] = 'Create new Performance Indicator'
            indFrm = indicatorForm()
            indFrm.indicatorMeasurementFrequency.choices = frequencyList()
            indFrm.indicatorUOM.choices = uomList()
            indFrm.indicatorProcessType.choices = processTypeList()
            indFrm.indicatorIndicatorType.choices = indicatorTypeList()
            indFrm.indicatorGoodPerformance.choices = goodPerformanceList()
            indFrm.indicatorOwner.choices = userList()
            indFrm.indicatorResponsible.choices = userList()

            if indFrm.validate_on_submit():
                try:
                    if indFrm.indicatorMeasurementFrequency.data == '':
                        indicatorMeasurementFrequency = None
                    else:
                        indicatorMeasurementFrequency = int(indFrm.indicatorMeasurementFrequency.data)
                    if indFrm.indicatorUOM.data == '':
                        indicatorUOM = None
                    else:
                        indicatorUOM = int(indFrm.indicatorUOM.data)
                    if indFrm.indicatorProcessType.data == '':
                        indicatorProcessType = None
                    else:
                        indicatorProcessType = int(indFrm.indicatorProcessType.data)
                    if indFrm.indicatorIndicatorType.data == '':
                        indicatorIndicatorType = None
                    else:
                        indicatorIndicatorType = int(indFrm.indicatorIndicatorType.data)
                    if indFrm.indicatorGoodPerformance.data == '':
                        indicatorGoodPerformance = None
                    else:
                        indicatorGoodPerformance = int(indFrm.indicatorGoodPerformance.data)

                    indicatorOwner = indFrm.indicatorOwner.data

                    ind = indicator(uuid = unicode(UUID.uuid4()),
                                    title = unicode(indFrm.indicatorTitle.data),
                                    desc = unicode(indFrm.indicatorDesc.data),
                                    dataSource = unicode(indFrm.indicatorDataSource.data),
                                    measurementFrequency_id = indicatorMeasurementFrequency,
                                    UOM_id = indicatorUOM,
                                    processType_id = indicatorProcessType,
                                    indicatorType_id = indicatorIndicatorType,
                                    goodPerformance_id = indicatorGoodPerformance,
                                    tenant_uuid = unicode(ten['uuid']))

                    owner = responsibilityAssignment(responsibilityObject_id = respObj.id,
                                                    reference_uuid = unicode(ind.uuid),
                                                    responsibilityType_id = respTypeOwner.id,
                                                    user_uuid = unicode(indicatorOwner))
                    db.session.add(owner)

                    responsible = indFrm.indicatorResponsible.data
                    for r in responsible:
                        resp = responsibilityAssignment(responsibilityObject_id = respObj.id,
                                            reference_uuid = unicode(ind.uuid),
                                            responsibilityType_id = respTypeResponsible.id,
                                            user_uuid = r)
                        db.session.add(resp)

                    db.session.add(ind)
                    db.session.commit()
                    successMessage('Indicator has been added')
                    return redirect(url_for('perfBP.indicatorListView'))

                except Exception as E:
                    if 'duplicate key value violates unique constraint' in unicode(E):
                        errorMessage('This indicator already exists')
                    else:
                        errorMessage(unicode(E))
            return render_template('performance/indicatorForm.html', indicatorForm=indFrm, **kwargs)

        elif function == 'update' and uuid != None:
            kwargs['contentTitle'] = 'Modify existing Performance Indicator'
            ind = indicator.query.filter_by(uuid=uuid, tenant_uuid=unicode(ten['uuid'])).first()

            owner = responsibilityAssignment.query.filter_by(responsibilityObject_id = respObj.id,
                                                    reference_uuid = unicode(ind.uuid),
                                                    responsibilityType_id = respTypeOwner.id).first()

            resp = responsibilityAssignment.query.filter_by(responsibilityObject_id = respObj.id,
                                                    reference_uuid = unicode(ind.uuid),
                                                    responsibilityType_id = respTypeResponsible.id).all()

            indFrm = indicatorForm(indicatorTitle = ind.title,
                                   indicatorDesc = ind.desc,
                                   indicatorDataSource = ind.dataSource,
                                   indicatorMeasurementFrequency = ind.measurementFrequency_id,
                                   indicatorUOM = ind.UOM_id,
                                   indicatorProcessType = ind.processType_id,
                                   indicatorIndicatorType = ind.indicatorType_id,
                                   indicatorGoodPerformance = ind.goodPerformance_id,
                                   indicatorOwner = owner.user_uuid if owner else None,
                                   indicatorResponsible = [r.user_uuid for r in resp] if resp else None)

            indFrm.indicatorMeasurementFrequency.choices = frequencyList()
            indFrm.indicatorUOM.choices = uomList()
            indFrm.indicatorProcessType.choices = processTypeList()
            indFrm.indicatorIndicatorType.choices = indicatorTypeList()
            indFrm.indicatorGoodPerformance.choices = goodPerformanceList()
            indFrm.indicatorOwner.choices = userList()
            indFrm.indicatorResponsible.choices = userList()

            if indFrm.validate_on_submit():
                try:
                    if indFrm.indicatorMeasurementFrequency.data == '':
                        indicatorMeasurementFrequency = None
                    else:
                        indicatorMeasurementFrequency = int(indFrm.indicatorMeasurementFrequency.data)
                    if indFrm.indicatorUOM.data == '':
                        indicatorUOM = None
                    else:
                        indicatorUOM = int(indFrm.indicatorUOM.data)
                    if indFrm.indicatorProcessType.data == '':
                        indicatorProcessType = None
                    else:
                        indicatorProcessType = int(indFrm.indicatorProcessType.data)
                    if indFrm.indicatorIndicatorType.data == '':
                        indicatorIndicatorType = None
                    else:
                        indicatorIndicatorType = int(indFrm.indicatorIndicatorType.data)
                    if indFrm.indicatorGoodPerformance.data == '':
                        indicatorGoodPerformance = None
                    else:
                        indicatorGoodPerformance = int(indFrm.indicatorGoodPerformance.data)

                    if not ind.title == indFrm.indicatorTitle.data:
                        if indicator.query.filter_by(title=indFrm.indicatorTitle.data, tenant_uuid=unicode(ten['uuid'])).first():
                            errorMessage('An indicator with this name already exists')

                    else:
                        responsible = indFrm.indicatorResponsible.data
                        resp = responsibilityAssignment.query.filter_by(responsibilityObject_id = respObj.id,
                                                reference_uuid = unicode(ind.uuid),
                                                responsibilityType_id = respTypeResponsible.id).all()
                        for r in resp:
                            db.session.delete(r)
                            db.session.commit()

                        for r in responsible:
                            resp = responsibilityAssignment(responsibilityObject_id = respObj.id,
                                                reference_uuid = unicode(ind.uuid),
                                                responsibilityType_id = respTypeResponsible.id,
                                                user_uuid = r)
                            db.session.add(resp)

                        newOwner = indFrm.indicatorOwner.data
                        if not newOwner:
                            db.session.delete(owner)

                        elif not owner:
                            owner = responsibilityAssignment(responsibilityObject_id = respObj.id,
                                                    reference_uuid = unicode(ind.uuid),
                                                    responsibilityType_id = respTypeOwner.id,
                                                    user_uuid = unicode(newOwner))
                            db.session.add(owner)
                        else:
                            owner.user_uuid = newOwner

                        ind.title = unicode(indFrm.indicatorTitle.data)
                        ind.desc = unicode(indFrm.indicatorDesc.data)
                        ind.dataSource = unicode(indFrm.indicatorDataSource.data)
                        ind.measurementFrequency_id = indicatorMeasurementFrequency
                        ind.UOM_id = indicatorUOM
                        ind.processType_id = indicatorProcessType
                        ind.indicatorType_id = indicatorIndicatorType
                        ind.goodPerformance_id = indicatorGoodPerformance

                        db.session.commit()
                        successMessage('Indicator has been modified')
                        return redirect(url_for('perfBP.indicatorListView'))

                except Exception as E:
                    if 'duplicate key value violates unique constraint' in unicode(E):
                        errorMessage('This indicator already exists')
                    else:
                        errorMessage(unicode(E))

            return render_template('performance/indicatorForm.html', indicatorForm=indFrm, **kwargs)
        elif function == 'delete' and uuid != None:
            ind = indicator.query.filter_by(uuid=request.form['uuid'], tenant_uuid=unicode(ten['uuid'])).first()

            db.session.delete(ind)
            db.session.commit()
            successMessage('The indicator has been deleted')
            return redirect(url_for('perfBP.indicatorListView'))
    else:
        errorMessage('Cannot verify your account, please log in again')
        return redirect(url_for('indexView'))

@perfBP.route('/target/', methods=['GET', 'POST'])
@loginRequired
@requiredRole([u'Superuser', u'Administrator'])
def indicatorTargetView(uuid=None, function=None):
    kwargs = {'title':'Indicator Targets',
              'contentTitle':''}
    ten = getCurrentTenant()
    if ten:

        if g.sijax.is_sijax_request:
            g.sijax.register_object(SijaxHandler)
            return g.sijax.process_request()

        indicators = selectIndicatorForm()
        indicators.indicator.choices = indicatorList()
        targetForm = newIndicatorTarget()

        if targetForm.validate_on_submit():
            pass

        return render_template('performance/indicatorTargetView.html', indicators=indicators, targetForm=targetForm, **kwargs)
    else:
        errorMessage('Cannot verify your account, please log in again')
        return redirect(url_for('indexView'))
