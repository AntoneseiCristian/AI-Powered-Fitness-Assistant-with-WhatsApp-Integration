
from twilio.rest import Client

def send_whatsapp_message(message):
    account_sid = 'ACa96dca1ec5a81f61bd6e93a7e8d74bfd'
    auth_token = 'e41b2ff769037315efc7943008d76261'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to='whatsapp:+40747709085'
    )



