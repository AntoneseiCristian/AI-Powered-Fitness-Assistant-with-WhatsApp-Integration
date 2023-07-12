from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_babel import Babel, _
from database import db, UserProfile  # Import db and UserProfile from database.py
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired
from whatsapp_message import send_whatsapp_message

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bmi_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize db with the app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'landing'  # Updated to 'landing'

babel = Babel()

def get_locale():
    return session.get('lang', 'en')

babel.init_app(app, locale_selector=get_locale)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Import BMIRecord after User has been defined
from BMIRecord import BMIRecord

User.bmi_records = db.relationship('BMIRecord', backref='user', lazy=True)

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    height = FloatField('Height', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')])
    activity_level = SelectField('Activity Level', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    submit = SubmitField('Save')

with app.app_context():
    db.create_all()

@app.route('/setlang/<lang>')
def setlang(lang):
    session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

@app.route('/landing', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Login failed. Check your username and/or password.', 'danger')
    return render_template('landing.html')

from sqlalchemy.exc import IntegrityError

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the username already exists
    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists. Please choose a different one.')
        return redirect(url_for('register'))

    # If the username doesn't exist, create a new user
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    try:
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('landing'))  # Redirect to 'landing' instead of 'login'
    except IntegrityError:
        db.session.rollback()
        flash('Username already exists. Please choose a different one.')
        return redirect(url_for('register'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    return redirect(url_for('landing'))

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # Get the user's profile
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    height = profile.height if profile else None

    # Get the latest BMI record of the current user
    bmi_record = BMIRecord.query.filter_by(user_id=current_user.id).order_by(BMIRecord.date.desc()).first()
    bmi = bmi_record.bmi if bmi_record else None
    recommendation = ''
    if request.method == 'POST' and 'weight' in request.form and 'height' in request.form:
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        bmi = calculate_bmi(weight, height)
        recommendation = get_recommendation(bmi)
        # Create a new BMIRecord and save it to the current user
        new_bmi_record = BMIRecord(bmi=bmi, weight=weight, height=height, user_id=current_user.id)  # Set weight and height
        db.session.add(new_bmi_record)
        db.session.commit()
    return render_template('index.html', bmi=bmi, recommendation=recommendation, bmi_record=bmi_record, height=height)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('landing'))

@app.route('/history', methods=['GET'])
@login_required
def history():
    # Query the database for all of the current user's BMI records, ordered by date
    bmi_records = BMIRecord.query.filter_by(user_id=current_user.id).order_by(BMIRecord.date.desc()).all()

    # Prepare the data for the chart
    dates = [record.date.strftime('%Y-%m-%d') for record in bmi_records]
    bmis = [record.bmi for record in bmi_records]

    return render_template('history.html', bmi_records=bmi_records, dates=dates, bmis=bmis)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Get the user's profile
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()

    # If a profile exists, pre-populate the form with the saved data
    if profile:
        form = ProfileForm(obj=profile)
    else:
        form = ProfileForm()

    if form.validate_on_submit():
        if not profile:
            # If a profile doesn't exist, create a new one
            profile = UserProfile(user_id=current_user.id)
        # Update the profile with the form data
        form.populate_obj(profile)
        db.session.add(profile)
        db.session.commit()
        flash('Profile saved successfully.')
        return redirect(url_for('index'))
    return render_template('profile.html', form=form)

def calculate_bmi(weight, height):
    send_whatsapp_message()
    return round(weight / ((height / 100) ** 2), 2)


def get_recommendation(bmi):
    if bmi < 18.5:
        return _("You are underweight. It's recommended to consult a nutritionist for a balanced diet plan.")
    elif 18.5 <= bmi < 25:
        return _("You have a normal weight. Keep maintaining a balanced diet and regular physical activity.")
    elif 25 <= bmi < 30:
        return _("You are overweight. Consider a balanced diet and regular physical activity. Consult a healthcare professional if needed.")
    else:
        return _("You are in the obesity range. It's highly recommended to consult a healthcare professional for guidance and support.")

if __name__ == "__main__":
    app.run(debug=True)
