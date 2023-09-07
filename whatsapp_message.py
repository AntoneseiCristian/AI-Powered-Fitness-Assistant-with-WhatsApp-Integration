from flask_login import current_user, login_required
from twilio.rest import Client
from database import UserProfile

@login_required
def send_whatsapp_message(message):

    profile = UserProfile.query.filter_by(user_id=current_user.id).first()

    # Get the phone number from profile.html page
    phone_number_from_profile = profile.phone_number
    # Get the account_sid and auth_token from the profile
    account_sid = profile.account_sid
    auth_token = profile.auth_token
    # print(account_sid)
    # print(auth_token)
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=f'whatsapp:{phone_number_from_profile}'
    )



