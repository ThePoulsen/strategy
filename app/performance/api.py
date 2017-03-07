from flask import Blueprint, jsonify, render_template, g, session
from app.admin.services import requiredRole, loginRequired
from app.crud.tenantCRUD import getCurrentTenant
from app.crud.userCRUD import getUser
from models import indicator
from app.masterData.models import measurementFrequency, UOM, processType, indicatorType, goodPerformance
import requests, flask_sijax
from app.sijax.handler import SijaxHandler
from app.chart.models import chartContainer

APIperfBP = Blueprint('APIperfBP', __name__, template_folder='templates')

@APIperfBP.route('/indicatorList', methods = ['GET'])
@loginRequired
@requiredRole([u'User', u'Superuser', u'Administrator'])
def getIndicatorListAPI():
    ten = getCurrentTenant()
    if ten:
        try:
            indicatorList = indicator.query.filter_by(tenant_uuid = ten['uuid']).all()
            indicatorDict = [{'title':t.title,
                              'uuid':t.uuid,
                              'desc':t.desc,
                              'dataSource':t.dataSource,
                              'measurementFrequency': measurementFrequency.query.get(t.measurementFrequency_id).title,
                              'UOM': UOM.query.get(t.UOM_id).title,
                              'processType': processType.query.get(t.processType_id).title,
                              'indicatorType': indicatorType.query.get(t.indicatorType_id).title,
                              'goodPerformance': goodPerformance.query.get(t.goodPerformance_id).title,
                              'targets':[{'uuid':ta.uuid, 
                                          'validFrom':ta.validFrom, 
                                          'validTo':ta.validTo,
                                          'fromTarget':ta.fromTarget,
                                          'toTarget':ta.toTarget,
                                          'timestamp':ta.timestamp} for ta in t.targets]} for t in indicatorList]

            return jsonify({'success':'Query ran successfully',
                            'indicators':indicatorDict})
        except Exception as E:
            return jsonify({'error': 'an error has ocurred and prevents the query to run'})
    else:
        return jsonify({'error':'Cannot verify your account, please log in again'})
    
@APIperfBP.route('/indicatorDetails/<string:uuid>', methods = ['GET'])
@loginRequired
@requiredRole([u'User', u'Superuser', u'Administrator'])
def getIndicatorDetailsAPI(uuid):
    ten = getCurrentTenant()
    if ten:
        try:
            ind = indicator.query.filter_by(tenant_uuid = ten['uuid'], uuid=uuid).first()
            indicatorDict = {'title':ind.title,
                              'uuid':ind.uuid,
                              'desc':ind.desc,
                              'dataSource':ind.dataSource,
                              'measurementFrequency': measurementFrequency.query.get(ind.measurementFrequency_id).title,
                              'UOM': UOM.query.get(ind.UOM_id).title,
                              'processType': processType.query.get(ind.processType_id).title,
                              'indicatorType': indicatorType.query.get(ind.indicatorType_id).title,
                              'goodPerformance': goodPerformance.query.get(ind.goodPerformance_id).title,
                              'targets':[{'uuid':t.uuid, 
                                          'validFrom':t.validFrom, 
                                          'validTo':t.validTo,
                                          'fromTarget':t.fromTarget,
                                          'toTarget':t.toTarget,
                                          'timestamp':t.timestamp} for t in ind.targets]}

            return jsonify({'success':'Query ran successfully',
                            'indicator details':indicatorDict})
        except Exception as E:
            if unicode(E) == "'NoneType' object has no attribute 'title'":
                return jsonify({'error': 'indicator not found'})
            else:
                return jsonify({'error': unicode(E)})
    else:
        return jsonify({'error':'Cannot verify your account, please log in again'})
    

    
@flask_sijax.route(APIperfBP, '/container')
def container():
    if g.sijax.is_sijax_request:
        g.sijax.register_object(SijaxHandler)
        return g.sijax.process_request()

    tenant = session['tenant_uuid']
    user = session['user_uuid']

    ind = indicator.query.filter_by(tenant_uuid=tenant).first()

    try:
        container = chartContainer.query.filter_by(tenant_uuid=tenant, indicator_id=ind.id, user_uuid=user).first()
        container_id = container.id
    except:
        container = chartContainer.query.filter_by(tenant_uuid=tenant, indicator_id=ind.id, user_uuid=None).first()
        container_id = container.id
        
    print container.id
    
    kwargs = {'containerTitle':container.title,
              'containerID':container.id,
              'initialSize': container.containerSize.size}
    
    container1 = (1, render_template('container/chartContainer.html', **kwargs))

    
    containerList=[container1]
    data = u''
    for c in containerList:
        data = data + unicode(c[1])
    
    kwargs = {'baseContent':data}
    return render_template('base.html', **kwargs)
