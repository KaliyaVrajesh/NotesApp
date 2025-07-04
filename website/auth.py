from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.Password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember='True')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Email or Password, Try Again', category='error')
        else:
            flash('User doesnt exists!', category = 'error')
        

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('first name')
        password1 = request.form.get('password1')
        password2 = request.form.get('confirm password')

        # if not email or not firstName or not password1 or not password2:
        #     flash('All fields are required.', category='error')       
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')
        elif len(email) < 5:
            flash('Email must be greater than 5 characters.', category = 'error')
        elif len(firstName) < 2:
            flash('FirstName must be greater than 2 characters.', category = 'error')
        elif len(password1) < 8:
            flash('Length of password must be greater than 8 characters.', category = 'error')
        elif password1 != password2:
            flash('Password and confirm password should be sane.', category = 'error')
        else:
            new_user = User(email=email, firstName=firstName, Password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember='True')
            flash('Account created successfully', category = 'success')
            return redirect(url_for('views.home'))



    return render_template("signup.html", user=current_user)

@auth.route('/insecure_reset', methods=['GET', 'POST'])
def insecure_reset():
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            user.Password = generate_password_hash(new_password)
            db.session.commit()
            flash("Password reset successfully (insecure method)", category='success')
        else:
            flash("Email not found", category='error')

        return redirect(url_for('auth.login'))

    return render_template('insecure_reset.html')

