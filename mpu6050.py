""" mpu6050.py: Configures and read/writes to an MPU6050 accelerometer/gyroscope. """

import smbus			

class MPU6050():
    def __init__(self):
        # Set register values
        self.define_registers()

        # Open the Raspberry Pi i2c bus
        self.bus = smbus.SMBus(1) 	

        # Set address of i2c bus
        self.ADDRESS = 0x68  

        # Set scaling constants
        self.SCALE_ACCEL = 16384.0
        self.SCALE_GYRO = 131.0

        self.start()

    def define_registers(self):
        # Define MPU6050 registers
        self.PWR_MGMT_1   = 0x6B
        self.SMPLRT_DIV   = 0x19
        self.CONFIG       = 0x1A
        self.GYRO_CONFIG  = 0x1B
        self.ACCEL_XOUT_H = 0x3B
        self.ACCEL_YOUT_H = 0x3D
        self.ACCEL_ZOUT_H = 0x3F
        self.GYRO_XOUT_H = 0x43
        self.GYRO_YOUT_H = 0x45
        self.GYRO_ZOUT_H = 0x47

    def start(self):
        # Disable Digital Low-Pass Filter, Gyroscope Output Rate = 8kHz
        self.bus.write_byte_data(self.ADDRESS, self.CONFIG, 0)

        # Sample Rate = Gyroscope Output Rate / (1 + SMPLRT_DIV) = 1kHz
        self.bus.write_byte_data(self.ADDRESS, self.SMPLRT_DIV, 7)
        
        # Use interal 8MHz oscillator for clock
        self.bus.write_byte_data(self.ADDRESS, self.PWR_MGMT_1, 1)
        
        # Full scale range = +/- 2000 deg/s
        self.bus.write_byte_data(self.ADDRESS, self.GYRO_CONFIG, 24)

    def read_raw_data(self, addr):
	# Accel and gyro value are 16-bit
        # Ex: ACCEL_XOUT_H = 3B, ACCEL_XOUT_L = 3C
        high_bits = self.bus.read_byte_data(self.ADDRESS, addr)
        low_bits = self.bus.read_byte_data(self.ADDRESS, addr + 1)
    
        # Concatenate higher and lower value
        value = (high_bits << 8) | low_bits
        
        # Convert to signed value
        if (value > 32768):
            value = value - 65536

        return value

    def read_data(self):
        # Read and scale data from the MPU6050
        acc_x = self.read_raw_data(self.ACCEL_XOUT_H) / self.SCALE_ACCEL
        acc_y = self.read_raw_data(self.ACCEL_YOUT_H) / self.SCALE_ACCEL
        acc_z = self.read_raw_data(self.ACCEL_ZOUT_H) / self.SCALE_ACCEL
        gyro_x = self.read_raw_data(self.GYRO_XOUT_H) / self.SCALE_GYRO
        gyro_y = self.read_raw_data(self.GYRO_YOUT_H) / self.SCALE_GYRO
        gyro_z = self.read_raw_data(self.GYRO_ZOUT_H) / self.SCALE_GYRO

        data = [acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z]
        return data

if __name__ == "__main__":
    device = MPU6050()
    data = device.read_data()
    print(data)
