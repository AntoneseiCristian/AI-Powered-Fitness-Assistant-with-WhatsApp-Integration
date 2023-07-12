# whatsapp_message.py

from twilio.rest import Client

def send_whatsapp_message():
    account_sid = '#'
    auth_token = '*'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+x',
        body="Don't forget to drink water",
        to='whatsapp:+40747709085'
    )

    print(message.sid)