from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import *
from sqlalchemy import desc
from datetime import datetime, date


auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()

        if user:
            if check_password_hash(user.password, password):

      
                login_user(user, remember=True)
            
                return redirect(url_for('views.homepage'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Wala dito account mo HAHA', category='error')

    return redirect(url_for('views.index_page'))

        
    
     
@auth.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birthday_str = request.form.get('birthday')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()

        user = User.query.filter_by(email = email).first()
        username = User.query.filter_by(firstName = first_name).first()

        if user:
            flash('Email is already exist', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 characters', category='error')
        elif len(last_name) < 1:
            flash('Last name must be greater than 1 character', category='error')
        elif len(address) < 5:
            flash('Address must be greater than 4 character', category='error')
        elif password1 != password2:
            flash('Password do not match', category='error')
        elif len(password1) < 8:
            flash('Password must be 8 characters or more', category='error')
        elif username:
            flash('Name is already taken, please find someone else', category='error')
        else:

            new_user = User(email = email, firstName = first_name, lastName = last_name, birthday = birthday, address = address, password = generate_password_hash(password1, method='pbkdf2:sha256'))
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            return redirect(url_for('views.homepage'))
            
           

        
        return redirect(url_for('views.index_page'))
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index_page'))

