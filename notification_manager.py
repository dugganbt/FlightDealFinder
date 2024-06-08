from twilio.rest import Client
from dotenv import load_dotenv
import os

# load twilio parameters
load_dotenv(".env")

# twilio parameters
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
to_number = os.getenv("to_number")
from_number = os.getenv("from_number")


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def __init__(self, account_sid=account_sid, auth_token=auth_token, from_number=from_number, to_number=to_number):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        self.to_number = to_number

    def send_notification_whatsapp(self, message_text):
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            from_=self.from_number,
            body=message_text,
            to=self.to_number
        )