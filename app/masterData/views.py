## -*- coding: utf-8 -*-
## project/app/admin/views.py

from app import db
from flask import Blueprint, render_template, request, redirect, url_for, session, g
from app.admin.services import requiredRole, loginRequired

mdBP = Blueprint('mdBP', __name__, template_folder='templates')

