from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_babel import Babel, _
from database import db  # Import db from database.py

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

with app.app_context():
    db.create_all()

@app.route('/setlang/<lang>')
def setlang(lang):
    session['lang'] = lang
    return redirect(url_for('index'))

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

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Check if password and confirm password match
    if password != confirm_password:
        flash('Passwords do not match.', 'danger')
        return redirect(url_for('landing') + '?register=true')

    hashed_password = generate_password_hash(password, method='scrypt')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash('Registration successful. You can now log in.', 'success')
    return redirect(url_for('landing'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing'))

@app.route('/')
@login_required
def home():
    return redirect(url_for('landing'))

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
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
        new_bmi_record = BMIRecord(bmi=bmi, user_id=current_user.id)
        db.session.add(new_bmi_record)
        db.session.commit()
    return render_template('index.html', bmi=bmi, recommendation=recommendation, bmi_record=bmi_record)




def calculate_bmi(weight, height):
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
