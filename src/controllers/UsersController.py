from flask import render_template, request, redirect, url_for
from flask_login import current_user
from src.models.UsersModel import User, db

def create():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        account = request.form['account']
        password = request.form['password']
        
        user = User(
            user_firstname = firstname,
            user_lastname = lastname,
            user_email = email,
            user_account = account,
            user_password = password,
            user_is_active = 1,
            user_is_deleted = 0
        )
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('app_routes.login'))

    return render_template('users/create.html', current_user=current_user)

def read():
    return render_template('index.html')

def update():
    return render_template('index.html')

def delete():
    return render_template('index.html')