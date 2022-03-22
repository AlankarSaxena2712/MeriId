from django.conf import settings
import twilio
from twilio.rest import Client

def send_twilio_message(to_number, body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    return client.messages.create(
        body=body,
        to=f"+91{to_number}",
        from_=settings.TWILIO_PHONE_NUMBER
    )