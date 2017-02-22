## -*- coding: utf-8 -*-
from flask import Blueprint, session, render_template, url_for, jsonify, json, g, redirect
from app.admin.services import sendMail, loginRequired, requiredRole, successMessage, errorMessage, apiMessage
from forms import registerForm, setPasswordForm, loginForm
import requests
from authAPI import authAPI

authBP = Blueprint('authBP', __name__, template_folder='templates')

# register
@authBP.route('/register', methods=['GET','POST'])
def registerView():
    if not 'token' in session:
        # universal variables
        form = registerForm()
        kwargs = {'formWidth':400}

        if form.validate_on_submit():
            dataDict = {'regNo' : form.regNo.data,
                        'companyName' : form.companyName.data,
                        'userName' : form.userName.data,
                        'email' : form.email.data,
                        'password' : form.password.data}

            req = authAPI('register', method='post', dataDict=dataDict)

            if 'error' in req:
                if req['error'] == 'Could not identify Platform':
                    errorMessage(req['error'])
                elif req['error'] == 'Request data incomplete':
                    errorMessage(req['error'])
                elif req['error'] == 'Reg/VAT number already exist':
                    errorMessage('An account using this Reg/VAT number already exist')
                elif req['error'] == 'Invalid email-address':
                    errorMessage(req['error'])
                elif req['error'] == 'Illegal null values present in request data':
                    errorMessage(req['error'])
                elif req['error'] == 'Internal server error':
                    errorMessage(req['error'])

            elif 'success' in req:
                # send email confirmation
                subject = u'Please confirm your account'
                tok = req['token']
                email = req['email']
                confirm_url = url_for('authBP.confirmEmailView',token=tok, _external=True)
                html = render_template('email/verify.html', confirm_url=confirm_url)

                sendMail(subject=subject,
                         sender='Henrik Poulsen',
                         recipients=[email],
                         html_body=html,
                         text_body = None)
                successMessage('You have successfully registered your account, please check your email for confirmation.')
                return redirect(url_for('indexView'))

        return render_template('auth/registerForm.html', form=form, **kwargs)
    else:
        errorMessage('alreadyRegistered')
        return redirect(url_for('indexView'))

# Confirmation mail redirect
@authBP.route('/confirm/<token>')
def confirmEmailView(token):
    session.clear()
    req = authAPI('confirm', method='post', token=token)
    if 'error' in req:
        if req['error'] == 'Could not identify access token':
            errorMessage(req['error'])

        elif req['error'] == 'Could not identify Platform':
            errorMessage(req['error'])

        elif req['error'] == 'User must set password':
            errorMessage('Please set your password')
            return redirect(url_for('authBP.setPasswordView', tok=req['token']))

        elif req['error'] == 'User already confirmed':
            errorMessage('Your profile has already been confirmed')
            return redirect(url_for('indexView'))

        else:
            errorMessage(req['error'])

    elif 'success' in req:
        if req['mustSetPass'] == 'True':
            successMessage('Your profile has been confirmed, please set your new password')
            return redirect(url_for('authBP.setPasswordView', tok=req['token']))
        else:
            successMessage('Your profile has been confirmed, please login')
            return redirect(url_for('authBP.loginView'))

    return redirect(url_for('indexView'))

# Set password

@authBP.route('/setPassword/<string:tok>', methods=['GET','POST'])
def setPasswordView(tok):
    if session['token']:
        session['token'] = None
    kwargs = {'formWidth':300,
              'title':'Set new password'}

    form = setPasswordForm()

    if form.validate_on_submit():
        dataDict={'password':form.password.data}
        print form.password.data
        req = authAPI('setPassword', method='post', dataDict=dataDict, token=tok)
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

            else:
                errorMessage(req['error'])
        elif 'success' in req:
            successMessage('Your password has now been set, please login')
            return redirect(url_for('authBP.loginView'))

    return render_template('auth/setPasswordForm.html', form=form, **kwargs)

# Login
@authBP.route('/login', methods=['GET','POST'])
def loginView():
    if not 'token' in session:
        kwargs = {'formWidth':300,
                  'contentTitle':'Login'}

        form = loginForm()
        if form.validate_on_submit():
            regNo = form.regNo.data
            email = form.email.data
            password = form.password.data

            dataDict = {'regNo':regNo,
                        'email':email,
                        'password':password}

            req = authAPI('login', method='post', dataDict=dataDict)
            if 'success' in req:
                session['token'] = req['token']
                session['email'] = req['email']
                session['roles'] = req['roles']
                successMessage('You are now logged in')
                return redirect(url_for('indexView'))
            elif 'error' in req:
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

                elif req['error'] == 'Internal server error':
                    errorMessage(req['error'])

                elif req['error'] == 'User is locked out of the system due to multiple bad logins':
                    errorMessage(req['error'])

                elif req['error'] == 'Could not identify Tenant':
                    errorMessage('We are not able to validate your credentials')

                elif req['error'] == 'Could not identify User':
                    errorMessage('We are not able to validate your credentials')

                elif req['error'] == 'Wrong user/password combination':
                    errorMessage(req['error']+' - Attempts left: '+req['attempts left'])

                elif req['error'] == 'User must change password':
                    session['token'] = req['token']
                    session['email'] = req['email']
                    session['roles'] = req['roles']
                    errorMessage('Please change your password')
                    return redirect(url_for('userBP.changePasswordView'))

        return render_template('auth/loginForm.html', form=form, **kwargs)
    else:
        errorMessage('You are already logged into the system')
        return redirect(url_for('indexView'))

# Logout
@authBP.route('/logout', methods=['GET','POST'])
def logoutView():
    logout = authAPI(endpoint='logout', method='post', token=session['token'])

    if ['error'] in logout:
        if req['error'] == 'Could not identify access token':
            errorMessage(req['error'])

        elif req['error'] == 'Could not identify Platform':
            errorMessage(req['error'])

        elif req['error'] == 'Internal server error':
            errorMessage(req['error'])

        elif req['error'] == 'Invalid access token':
            errorMessage(req['error'])

    else:
        session.clear()
        successMessage('You are now logged out of the system')

    return redirect(url_for('indexView'))
