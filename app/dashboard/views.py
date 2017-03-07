## -*- coding: utf-8 -*-

from app import db
from flask import Blueprint, render_template, request, redirect, url_for, session, g
from app.admin.services import requiredRole, loginRequired

dashBP = Blueprint('dashBP', __name__, template_folder='templates')

# Admin view
@dashBP.route('/list')
@requiredRole([u'User', u'Superuser', u'Administrator'])
@loginRequired
def dashListView():
    kwargs = {'title':'Dashboards',
              'contentTitle':'Current dashboards',
              'targetButtons':False,
              'chartButtons':False,
              'tableColumns':['Dashboard','Description','Indicators']}

    return render_template('listView.html', **kwargs)
