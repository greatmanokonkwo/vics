"""
SIGNALS
---------
Left buzzer ON (continous) - Turn left by required degrees
Right buzzer ON (continous) - Turn right by the required degrees
Left and Right buzzer ON (4 secs) - Stop!
"""
import sys.os
sys.path.append("..")

import time
import smbus
from PIL import Image
import Jetson.GPIO as GPIO
import torch 
from torchvision import transforms

from imusensor.MPU9250 import MPU9250
from imusensor.filters import kalman

from devices.picam import picam
from neuralnet.GuideNet import GuideNet

class GuideSystem:
	# GPIO pins for the two information relay vibration motors
	LEFT_BUZZER = 35
	RIGHT_BUZZER = 7

	def __init__(self):
		# The Raspberry Pi Camera V2 for taking images 
		self.cam = picam(width=256, height=256)

		# Initialize and caliberate IMU sensor
		address = 0x68
		bus = smbus.SMBus(1)
		self.imu = MPU9250.MPU9250(bus, address)
		self.imu.begin()
	
		calib_file = "calib.json"

		# caliberate sensor with saved caliberation file
		if os.path.exists(calib_file):
			self.imu.loadCalibDataFromFile(calib_file)

		# IMU sensor fusion algorithm
		self.sensorfusion = kalman.Kalman()
		self.imu.readSensor()
		self.imu.computeOrientation()

		self.sensorfusion.roll = self.imu.roll			
		self.sensorfusion.pitch = self.imu.pitch
		self.sensorfusion.yaw = self.imu.yaw			

		self.INITIAL_YAW = self.imu.yaw # Magnetometer measures heading relative to true north, we need to meausure relative user's initial heading 
		self.prev_yaw = 0

		# Setup buzzer GPIO to output
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.LEFT_BUZZER, GPIO.OUT, initial=0)
		GPIO.setup(self.RIGHT_BUZZER, GPIO.OUT, initial=0)

		# Set inference model by loading the parameters where they have been saved
		device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
		self.model = GuideNet().to(device=device) 
		model_path = os.getcwd() + "/neuralnet/guide_net.pt"
		if os.path.exists(model_path):
			self.model.load_state_dict(torch.load(model_path))

		self.tensor = transforms.ToTensor()

	# The formula to calculate the range of the direction class is: (class*PI/8 - PI/2) +- PI/16
	def __get_direction_class_range(self, direct_class):
		class_angle = direct_class*22.5 - 90
		return (class_angle - 11.25, class_angle + 11.25)

	def run(self):
		"""
		# Collect image and run inference
		self.cam.save_image("captured.jpg")
		img = self.tensor(Image.open("capture.jpg"))
		direct_class = self.model(img.unsqueeze(0))[0]
		"""
		direct_class = 7

		# if halt signal is not inferred run direction signalling, else run halt signalling
		if direct_class != 9:
			# Get acceptable movement range for the specified direction class
			lower, upper = self.__get_direction_class_range(direct_class)

			# Direction signal involves turning on the buzzer that corresponds to the direction that the user is supposed to go to and continously vibrating it until the user has moved to the right angle
			buzzer = self.RIGHT_BUZZER if direct_class>4 else self.LEFT_BUZZER
			GPIO.output(buzzer, 1)
			
			currTime = time.time()	
			yaw_angle = 0
			print (upper, lower)
			time.sleep(3)
			while not (yaw_angle < upper and yaw_angle >= lower): # While displacement angle not in range of predict direction class
				# Calculate the displaced angle of user using IMU sensor
				self.imu.readSensor()
				self.imu.computeOrientation()
				newTime = time.time()
				dt = newTime - currTime
				currTime = newTime

				self.sensorfusion.computeAndUpdateRollPitchYaw(self.imu.AccelVals[0], self.imu.AccelVals[1], self.imu.AccelVals[2], self.imu.GyroVals[0], self.imu.GyroVals[1], self.imu.GyroVals[2], self.imu.MagVals[0], self.imu.MagVals[1], self.imu.MagVals[2], dt)

				yaw_angle = self.sensorfusion.yaw - self.INITIAL_YAW

			self.prev_yaw = yaw_angle
			GPIO.output(buzzer, 0)	
			
		else:
			# Stop signal for 3 seconds
			GPIO.output(self.RIGHT_BUZZER, 1)	
			GPIO.output(self.LEFT_BUZZER, 1)

			time.sleep(3)

			GPIO.output(self.RIGHT_BUZZER, 0)	
			GPIO.output(self.LEFT_BUZZER, 0)
	
		time.sleep(1)
	
	def cleanup():
		self.cam.cleanup()	

if __name__ == "__main__":
	system = GuideSystem()
	while True:
		system.run()
	system.cleanup()
