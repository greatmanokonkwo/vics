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

class GuideSystem:
	# IMU sensor
	sensorfusion = madgwick.Madgwick(0.5)
	imu = None

	# The Raspberry Pi Camera V2 for taking images 
	cam = None

	# GPIO pins for the two information relay vibration motors
	right_buzzer = 7
	left_buzzer = 37

	model = None

	prev_yaw = 0

	def __init__(self):
		# Initialize and caliberate IMU sensor
		address = 0x68
		bus = smbus.SMBus(1)
		self.imu = MPU9250.MPU9250(bus, address)
		self.imu.begin()
	
		self.imu.caliberateGyro()
		self.imu.caliberateAccelerometer()
		self.imu.caliberateMagPrecise()	
	
		# Setup buzzer GPIO to output
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.left_buzzer, GPIO.OUT, initial=0)
		GPIO.setup(self.right_buzzer, GPIO.OUT, initial=0)

		# Set inference model by loading the parameters where they have been saved
		device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
		self.model = GuideNet().to(device=device) 
		model_path = os.getcwd() + "/neuralnet/guide_net.pt"
		if os.path.exists():
			self.model.load_state_dict(torch.load(model_path))

	# TODO: Implement method for calculating the yaw of the on-board MPU9250 sensors
	def __calculate_yaw():

	# The formula to calculate the range of the direction class is: (class*PI/8 - PI/2) +- PI/16
	def get_direction_class_range(direct_class):
		class_angle = direct_class*22.5 - 90
		return (class_angle - 11.25, class_angle + 11.25)

	def run():
		# Collect image and run inference
		cam.save_image("captured.jpg")
		tensor = transforms.ToTensor()
		img = tensor(Image.open("capture.jpg"))
		direct_class = model(img.unsqueeze(0))[0]

		# if halt signal is not inferred run direction signalling, else run halt signalling
		if direct_class != 9:
			# Get acceptable movement range for the specified direction class
			lower, uppper = get_direction_class_range(direct_class)

			# Direction signal involves turning on the buzzer that corresponds to the direction that the user is supposed to go to and continously vibrating it until the user has moved to the right angle
			buzzer = right_buzzer if direct_class>4 else left_buzzer
			GPIO.output(buzzer, 1)
			
			yaw_angle = 0
			
			while !(yaw_angle > upper && yaw_angle <= lower):
				# Calculate the displaced angle of user using IMU sensor
				yaw_angle = __calculate_yaw() - self.prev_yaw
			
			self.prev_yaw = __calculate_yaw()
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
	system = GuideSystem()
 	while True:
		system.run()
