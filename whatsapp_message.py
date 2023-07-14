# whatsapp_message.py

from twilio.rest import Client

def send_whatsapp_message(message):
    account_sid = '#'
    auth_token = '*'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+$',
        body=message,
        to='whatsapp:+%'
    )

    print(message.sid)
