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
import torch 
from torchvision import transforms

from imusensor.MPU9250 import MPU9250
from imusensor.filters import madgwick

from neuralnet.GuideCNN import GuideCNN

class GuideSystem:
	# GPIO pins for the two information relay vibration motors
	LEFT_BUZZER = 23
	RIGHT_BUZZER = 11

	def __init__(self):
		# Initialize and caliberate IMU sensor
		address = 0x68
		bus = smbus.SMBus(1)
		self.imu = MPU9250.MPU9250(bus, address)
		self.imu.begin()
	
		calib_file = "/home/greatman/code/vics/devs_and_utils/calib.json"

		# caliberate sensor with saved caliberation file
		if os.path.exists(calib_file):
			self.imu.loadCalibDataFromFile(calib_file)

		# IMU sensor fusion algorithm
		self.sensorfusion = madgwick.Madgwick() 

		start_time = time.time()
		while time.time() - start_time < 12.5: # The IMU starts 
			self.calculate_yaw(time.time())
			self.INITIAL_YAW = self.sensorfusion.yaw # Magnetometer measures heading relative to true north, we need to meausure relative user's initial heading 
		self.prev_yaw = 0

		# Setup buzzer GPIO to output
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.LEFT_BUZZER, GPIO.OUT, initial=0)
		GPIO.setup(self.RIGHT_BUZZER, GPIO.OUT, initial=0)

		# Set inference model by loading the parameters where they have been saved
		#device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
		device = "cpu"
		self.model = GuideCNN().to(device=device) 
		model_path = os.getcwd() + "/neuralnet/guide_net.pt"
		if os.path.exists(model_path):
			self.model.load_state_dict(torch.load(model_path))

		self.tensor = transforms.ToTensor()
		self.softmax = torch.nn.Softmax(dim=0)

	# The formula to calculate the range of the direction class is: (class*PI/8 - PI/2) +- PI/16
	def __get_direction_class_range(self, direct_class):
		class_angle = direct_class*45 - 90
		return (class_angle - 22.5, class_angle + 22.5)

	def calculate_yaw(self, currTime):
	
		# Calculate the yaw angle of the mpu9250 device
		for i in range(10):
			newTime = time.time()
			dt = newTime - currTime
			currTime = newTime
				
			self.sensorfusion.updateRollPitchYaw(self.imu.AccelVals[0], self.imu.AccelVals[1], self.imu.AccelVals[2], self.imu.GyroVals[0], self.imu.GyroVals[1], self.imu.GyroVals[2], self.imu.MagVals[0], self.imu.MagVals[1], self.imu.MagVals[2], dt)

		return currTime

	def run(self, cam):
		
		try:
			# Collect image and run inference
			cam.save_image("capture.jpg")
			img = self.tensor(Image.open("capture.jpg"))
			direct_class = torch.max(self.softmax(self.model(img.unsqueeze(0))[0]), dim=0)[1].item()
	
			# if halt signal is not inferred run direction signalling, else run halt signalling
			if direct_class != 5:
				# Get acceptable movement range for the specified direction class
				lower, upper = self.__get_direction_class_range(direct_class)

				# Direction signal involves turning on the buzzer that corresponds to the direction that the user is supposed to go to and continously vibrating it until the user has moved to the right angle
				buzzer = self.RIGHT_BUZZER if direct_class>2 else self.LEFT_BUZZER
				GPIO.output(buzzer, GPIO.HIGH)
			
				currTime = time.time()	
				yaw_angle = 0
				print (upper, lower)
				time.sleep(3)
				while not (yaw_angle < upper and yaw_angle >= lower): # While displacement angle not in range of predict direction class
					# Calculate the displaced angle of user using IMU sensor
					self.imu.readSensor()
					self.calculate_yaw(currTime)
					yaw_angle = self.sensorfusion.yaw - self.INITIAL_YAW
					print(yaw_angle)

				self.prev_yaw = yaw_angle
				GPIO.output(buzzer, GPIO.LOW)	
			
			else:
				# Stop signal for 3 seconds
				GPIO.output(self.RIGHT_BUZZER, GPIO.HIGH)	
				GPIO.output(self.LEFT_BUZZER, GPIO.HIGH)

				time.sleep(3)

				GPIO.output(self.RIGHT_BUZZER, GPIO.LOW)	
				GPIO.output(self.LEFT_BUZZER, GPIO.LOW)
	
			time.sleep(1)
		
		finally:
			self.cleanup()	

	def cleanup(self):
		GPIO.cleanup()	

if __name__ == "__main__":
	system = GuideSystem()
	while True:
		system.run()
