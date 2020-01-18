""" detector.py: Main MotionDetector module, sends SMS alerts when motion is detected. """

import time, datetime

import config as cfg
from mpu6050 import MPU6050
from send_sms import SendSMS

class Detector():
    def __init__(self):
        # Read device settings from config file
        self.sensitivity_threshold = cfg.device_config['sensitivity_threshold']
        self.update_frequency_delay = cfg.device_config['update_frequency_delay']
        self.send_activation_msg = cfg.device_config['send_activation_msg']

        # Initialize the mpu6050
        self.mpu = MPU6050()

        # Initialize Twilio API
        self.sendsms = SendSMS()

        if (self.send_activation_msg):
            self.sendsms.send("Motion detector activated.",
                              self.sendsms.target_phone_number)

    def watch(self):
        print("Waiting for motion...")

        # Initialize prev_data with the first data sample
        prev_data = self.mpu.read_data()

        # Watch for changes in motion
        while True:
            data = self.mpu.read_data()

            # Check each reading in the data list for changes
            for i in range(5):

                diff = abs(data[i] - prev_data[i])

                # Compare the change with the sensitivity value
                if diff > self.sensitivity_threshold:
                    print("[Motion Detected] Magnitude:", diff)

                    # Get the current time (UTC)
                    self.time = str(datetime.datetime.now())

		    # Format the alert message
                    self.msg = "ALERT: Motion detected at " + self.time[11:19]

                    # Print and send the alert
                    print(self.msg)
                    self.alert(self.msg)

                    # Reset data values
                    data = [0, 0, 0, 0, 0, 0]

                    # Delay to avoid sending multiple alerts at once
                    time.sleep(5)
                    
            # Save data for next read cycle
            prev_data = data

            # Limit the data read cycle speed
            time.sleep(self.update_frequency_delay)
            
    def alert(self, msg):
        # Send alert message
        self.sendsms.send(self.msg, self.sendsms.target_phone_number)

if __name__ == "__main__":
    detector = Detector()
    detector.watch()