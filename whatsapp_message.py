from flask_login import current_user
from twilio.rest import Client
from database import UserProfile

def send_whatsapp_message(message):
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()

    # Get the account_sid and auth_token from the profile
    account_sid = profile.account_sid
    auth_token = profile.auth_token
    #print(account_sid)
    #print(auth_token)
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to='whatsapp:+40747709085'
    )



