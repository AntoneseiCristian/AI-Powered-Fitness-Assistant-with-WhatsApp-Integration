from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, jsonify
from flask_login import login_required, current_user
from models import User, BMIRecord
from forms import ProfileForm
from database import db, UserProfile
from datetime import datetime
from whatsapp_message import send_whatsapp_message
from language_model import get_response
from utils import calculate_bmi, get_recommendation, calculate_recommended_bmi_and_weight
from werkzeug.security import generate_password_hash, check_password_hash
from twilio.twiml.messaging_response import MessagingResponse

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home():
    return redirect(url_for('auth.landing'))

@main.route('/index', methods=['GET', 'POST'])
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
        previous_date = request.form.get('previous_date')
        previous_date = datetime.strptime(previous_date, '%Y-%m-%d') if previous_date else datetime.utcnow()
        bmi = calculate_bmi(weight, height)
        recommendation = get_recommendation(bmi)
        # Create a new BMIRecord and save it to the current user
        new_bmi_record = BMIRecord(bmi=bmi, weight=weight, height=height, user_id=current_user.id, date=previous_date)  # Set weight, height, and date
        db.session.add(new_bmi_record)
        db.session.commit()
    return render_template('index.html', bmi=bmi, recommendation=recommendation, bmi_record=bmi_record, height=height)


@main.route('/history', methods=['GET'])
@login_required
def history():
    # Query the database for all of the current user's BMI records, ordered by date
    bmi_records = BMIRecord.query.filter_by(user_id=current_user.id).order_by(BMIRecord.date.desc()).all()

    # Prepare the data for the chart
    dates = [record.date.strftime('%Y-%m-%d') for record in bmi_records]
    bmis = [record.bmi for record in bmi_records]

    # Get the user's profile
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    height = profile.height if profile else None

    # Calculate the recommended BMI and weight based on the user's height
    recommended_bmi, recommended_weight = calculate_recommended_bmi_and_weight(height) if height else (None, None)

    print(dates)  # Add this line to print the dates data
    print(bmis)  # Add this line to print the bmis data

    return render_template('history.html', bmi_records=bmi_records, dates=dates, bmis=bmis, recommended_bmi=recommended_bmi, recommended_weight=recommended_weight, height=height)

@main.route('/delete_record/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    record = BMIRecord.query.get(record_id)
    if record.user_id != current_user.id:
        abort(403)  # Forbidden
    db.session.delete(record)
    db.session.commit()
    flash('Record deleted successfully.')
    return redirect(url_for('main.history'))

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Get the user's profile
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    print(request.headers)
    print(request.data)
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
        return redirect(url_for('main.index'))
    return render_template('profile.html', form=form)

@main.route('/message', methods=['GET', 'POST'])
@login_required
def message():
    if request.method == 'POST':
        custom_message = request.form.get('message')
        send_whatsapp_message(custom_message)
        flash('Message sent successfully.')
        return redirect(url_for('main.message'))
    return render_template('message.html')

@main.route('/delete_all_records', methods=['POST'])
@login_required
def delete_all_records():
    password = request.form.get('password')
    user = User.query.filter_by(username=current_user.username).first()
    if user and check_password_hash(user.password, password):
        BMIRecord.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('All records deleted successfully.')
    else:
        flash('Incorrect password. Please try again.')
    return redirect(url_for('main.history'))

@main.route('/prompt', methods=['POST'])
@login_required
def prompt():
    if request.method == 'POST':
        prompt_message = request.json.get('message')
        print(f'Prompt: {prompt_message}')  # print the prompt message
        if prompt_message:
            response_message = get_response(prompt_message)
            print(f'Response: {response_message}')
            send_whatsapp_message(response_message)# print the response message
            return jsonify({"responseField": response_message})
        else:
            send_whatsapp_message("No prompt message provided")
            return jsonify({"error": "No prompt message provided"}), 400
    else:
        send_whatsapp_message("Invalid request method")
        return jsonify({"error": "Invalid request method"}), 405

@main.route("/receive-wapp-messages", methods=['POST'])
def receive_wapp_messages():

    # Get the message sent from WhatsApp
    incoming_msg = request.values.get('Body', '').lower()

    # Get the phone number the message is coming from
    from_number = request.values.get('From', '')

    # Remove the 'whatsapp:' prefix from the phone number
    from_number = from_number.replace('whatsapp:', '')


    # Print all request headers
    print("Headers:")
    print(request.headers)

    # Print all form data
    print("Form Data:")
    print(request.form)

    # Print all query parameters
    print("Query Parameters:")
    print(request.args)
    # Here you can process the message as needed, for example, save it to a database
    # or update your application state
    # Query the database for a user with this phone number
    user = UserProfile.query.filter_by(phone_number=from_number).first()

    # If no user is found, return a 403 Forbidden response
    if user is None:
        send_whatsapp_message("User has not completed his profile")
        abort(403)
    # Send a response back to WhatsApp
    resp = MessagingResponse()
    msg = resp.message()
    print(incoming_msg)
    msg.body("Received your message!")
    if incoming_msg:
        response_message = get_response(incoming_msg)
        print(f'Response: {response_message}')
        send_whatsapp_message(response_message)  # print the response message
        return jsonify({"responseField": response_message})
    return str(resp)

@main.route('/setlang/<lang>')
def setlang(lang):
    session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))