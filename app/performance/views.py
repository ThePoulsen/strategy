## -*- coding: utf-8 -*-
## project/app/admin/views.py

from app import db
from flask import Blueprint, render_template, request, redirect, url_for, session, g
from app.admin.services import requiredRole, loginRequired, errorMessage, successMessage
from models import indicator
from app.crud.tenantCRUD import getCurrentTenant

perfBP = Blueprint('perfBP', __name__, template_folder='templates')

@perfBP.route('/indicator', methods=['GET'])
@perfBP.route('/indicator/<string:function>', methods=['GET', 'POST'])
@perfBP.route('/indicator/<string:function>/<string:uuid>', methods=['GET', 'POST'])
@loginRequired
@requiredRole(u'Administrator')
def indicatorView(function=None, uuid=None):
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
