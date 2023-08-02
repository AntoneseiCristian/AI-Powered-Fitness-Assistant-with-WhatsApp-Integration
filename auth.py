from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from models import User
from database import db, UserProfile
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

auth = Blueprint('auth', __name__)

@auth.route('/landing', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.configure_twilio'))
        flash('Login failed. Check your username and/or password.', 'danger')
    return render_template('landing.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('auth.landing', register='true'))  # Include a query parameter in the URL

        # If the username doesn't exist, create a new user
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.landing'))  # Redirect to the landing page after successful registration
        except IntegrityError:
            db.session.rollback()
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('auth.landing', register='true'))  # Include a query parameter in the URL

    return render_template('landing.html')  # Render the landing page for a GET request

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.landing'))

