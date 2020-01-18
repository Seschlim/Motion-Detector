""" config.py: Configuration file for Motion Detector modules. """

# Twilio Account Settings
# Note: A valid Twilio account and associated phone number is required for operation
user_config = {'account_sid': '8888888888888888888888888888888888',
               'auth_token': '88888888888888888888888888888888',
               'account_phone_number': '+18888888888',
               'target_phone_number': '+18888888888' # Number to send SMS alerts to
               }

# Device Settings
device_config = {'sensitivity_threshold': 10, # Minimum change in acceleration required to trigger an alert
                 'update_frequency_delay': 0.1, # Delay time in seconds between each data read cycle
                 'send_activation_msg': True # Send an SMS alert when the system has successfully started
                 }
