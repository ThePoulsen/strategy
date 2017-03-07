from flask import Blueprint, jsonify, render_template, g
from app.admin.services import requiredRole, loginRequired
from app.crud.tenantCRUD import getCurrentTenant
from models import indicator
from app.masterData.models import measurementFrequency, UOM, processType, indicatorType, goodPerformance
import requests, flask_sijax
from app.sijax.handler import SijaxHandler

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
        
    
    kwargs = {'containerTitle':'Container 1',
              'containerUUID':unicode('3'),
              'initialSize': 'col-xs-12 col-sm-12 col-md-9 col-lg-9'}
    
    container1 = (1, render_template('container/chartContainer.html', **kwargs))
    
    kwargs = {'containerTitle':'Container 2',
              'containerUUID':unicode('4'),
              'initialSize': 'col-xs-12 col-sm-12 col-md-3 col-lg-3'}
   
    container2 = (2, render_template('container/chartContainer.html', **kwargs))
    
    containerList=[container1, container2]
    containerList.sort(key = lambda row: row[0])
    data = u''
    for c in containerList:
        data = data + unicode(c[1])
        
    
    kwargs = {'baseContent':data}
    return render_template('base.html', **kwargs)