""" send_sms.py: Use the Twilio SMS API to send text alerts to a target phone number. """

from twilio.rest import Client
import config as cfg

# Use the Twilio API to send SMS messages to the target device
class SendSMS():
    def __init__(self):
        # Read Twilio account info from config file
        self.account_sid = cfg.user_config['account_sid']
        self.auth_token = cfg.user_config['auth_token']
        self.account_phone_number = cfg.user_config['account_phone_number']
        self.target_phone_number = cfg.user_config['target_phone_number']

        # Start the Twilio client
        self.client = Client(self.account_sid, self.auth_token)

    def send(self, msg, phone_number):
        # Send an SMS message to the target phone number
        message = self.client.messages.create(
                      body = msg,
                      from_ = self.account_phone_number,
                      to = phone_number)
                    
        # Log the message ID to the console
        print("Sent message with ID: " + message.sid)

if __name__ == "__main__":
    sendsms = SendSMS()
    sendsms.send("Test Message", sendsms.target_phone_number)