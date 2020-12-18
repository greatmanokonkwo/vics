"""
SIGNALS
---------
Left buzzer ON (continous) - Turn left by required degrees
Right buzzer ON (continous) - Turn right by the required degrees
Left and Right buzzer ON (4 secs) - Stop!

"""

import time
import smbus
from PIL import Image
import Jetson.GPIO as GPIO
import os
import torch 
from torchvision import transforms
from imusensor.MPU9250 import MPU9250
from imusensor.filters import madgwick
from devices.picam import picam

# IMU sensor
sensorfusion = madgwick.Madgwick(0.5)
imu = None

# The Raspberry Pi Camera V2 for taking images 
cam = None

# GPIO pins for the two information relay vibration motors
right_buzzer = 7
left_buzzer = 37

model = None

def initialize(width=256, height=256):
	global imu, cam, motor1, motor2, model

	# Initialize and caliberate IMU sensor
	address = 0x68
	bus = smbus.SMBus(1)
	imu = MPU9250.MPU9250(bus, address)
	imu.begin()
	
	imu.caliberateGyro()
	imu.caliberateAccelerometer()
	imu.caliberateMagPrecise()	
	
	# Setup buzzer GPIO to output
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(left_buzzer, GPIO.OUT, initial=0)
	GPIO.setup(right_buzzer, GPIO.OUT, initial=0)

	# Set inference model by loading the parameters where they have been saved
	device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
	model = GuideNet().to(device=device) 
	model_path = os.getcwd() + "/neuralnet/guide_net.pt"
	if os.path.exists():
		model.load_state_dict(torch.load(model_path))

def calculate_yaw():
	currTime = time.time()
	imu.readSensor()
	for i in range(10):
		newTime = time.time()
		dt = newTime - currTime
		currTime = newTime

		sensorfusion.updateRollPitchYaw(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2], imu.GyroVals[0],
									imu.GyroVals[1], imu.GyroVals[2], imu.MagVals[0], imu.MagVals[1], imu.MagVals[2], dt)
	
	return sensorfusion.yaw

def guide_system_run():
	while True:
		# Collect image and run inference
		cam.save_image("captured.jpg")
		tensor = transforms.ToTensor()
		img = tensor(Image.open("capture.jpg"))
		angle, halt = model(img.unsqueeze(0))[0]

		# if halt signal is not inferred run direction signalling, else run halt signalling
		if halt <= 0.5:
			# Direction signal involves turning on the buzzer that corresponds to the direction that the user is supposed to go to and continously vibrating it until the user has moved to the right angle
			buzzer = right_buzzer if angle>0 else left_buzzer
			GPIO.output(buzzer, 1)
			
			prev_yaw = 0
			# If the displaced angle is within 2 degrees of predicted angle
			while abs(angle) >= 2:
				# Calculate the displaced angle of user using IMU sensor
				yaw = calculate_yaw()
				angle -= (yaw - prev_yaw) # subtract from the desired angle the change in angle of the user
				prev_yaw = yaw
			
			GPIO.output(buzzer, 0)	
			
		else:
			# Stop signal for 3 seconds
			GPIO.output(right_buzzer, 1)	
			GPIO.output(left_buzzer, 1)

			time.sleep(3)

			GPIO.output(right_buzzer, 0)	
			GPIO.output(left_buzzer, 0)
	
		time.sleep(1)

if __name__ == "__main__":
	initialize()
	guide_system_run()
