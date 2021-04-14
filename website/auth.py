from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from.models import RegisteredUser
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .views import views
import re

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = RegisteredUser.query.filter_by(email = email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                # redirect to home page
                return redirect(url_for('views.home'))

            else:
                flash('Incorrect Password', category='error')
        else:
            flash('Email does not exist, Please Register', category='error')
    return render_template('login.html', user = current_user)

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_type = request.form.get('user_type');

        # print(request.form.get('theatre_admin'))

        if password1 != password2:
            flash('Passwords not matching', category='error')
        elif len(name) < 3:
            flash('Name must be more than 2 Characters', category='error')
        else:
            user = RegisteredUser.query.filter_by(email = email).first()
            
            if user:
                flash('Account already exists, Please Login', category='warning')
            else:
                if bool(re.search('^[\w.+\-]+@bookmyshow\.com$', email)):
                    if user_type == "theatre_admin":
                        flash('You cannot use bookmyshow domain for other purposes', category='warning')
                        return render_template('sign_up.html', user = current_user)
                    else:
                        new_user = RegisteredUser(email = email, name = name, password = generate_password_hash(password1, method='sha256'), is_theatre_admin = False, is_super_admin = True)
                elif user_type == "theatre_admin":
                    new_user = RegisteredUser(email = email, name = name, password = generate_password_hash(password1, method='sha256'), is_theatre_admin = True, is_super_admin = False)
                else:
                    new_user = RegisteredUser(email = email, name = name, password = generate_password_hash(password1, method='sha256'), is_theatre_admin = False, is_super_admin = False)
                print(new_user)
                db.session.add(new_user)
                db.session.commit()
                # login_user(user, remember=True)
                flash('Account created!', category='success')
                
                # redirect to home page
                return redirect(url_for('views.home'))

    return render_template('sign_up.html', user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))