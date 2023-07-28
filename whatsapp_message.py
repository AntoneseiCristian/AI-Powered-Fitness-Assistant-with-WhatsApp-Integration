
from twilio.rest import Client

def send_whatsapp_message(message):
    account_sid = '#'
    auth_token = '$'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to='whatsapp:+40747709085'
    )



