"""
SIGNALS
---------
Left buzzer ON (continous) - Turn left by required degrees
Right buzzer ON (continous) - Turn right by the required degrees
Left and Right buzzer ON (4 secs) - Stop!

"""

import time
from PIL import Image
import Jetson.GPIO as GPIO
import os.getcwd
import torch.load
from torchvision import transforms.ToTensor
from devices.mpu9250 import mpu9250
from devices.picam import picam

# The MPU9250 sensor for calculating the displacement angle
#mpu9250 = mpu9250(0x68)

# The Raspberry Pi Camera V2 for taking images 
cam = None

# GPIO pins for the two information relay vibration motors
right_buzzer = 7
left_buzzer = 37

model = None

# Constants
E = 2

def initialize(width=256, height=256):
	global mpu, cam, motor1, motor2, model
	
	"""
	mpu.set_accel_range(mpu.ACCEL_RANGE_2G)
	mpu.set_gyro_range(mpu.GYRO_RANGE_2000DEG)
	
	cam = picam(width, height)
	"""
	
	# Setup buzzer GPIO to output
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(left_buzzer, GPIO.OUT)
	GPIO.setup(right_buzzer, GPIO.OUT)

	# Set inference model by loading the parameters where they have been saved
	"""
	device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
	model = GuideNet().to(device=device) 
	model_path = os.getcwd() + "/neuralnet/guide_net.pt"
	if os.path.exists():
		model.load_state_dict(torch.load(model_path))
	"""

def guide_system_run():
	while True:
		# Run inference
		"""
		cam.save_image("captured.jpg")
		tensor = transforms.ToTensor()
		img = tensor(Image.open("capture.jpg"))
		angle, halt = model(img)
		"""
		angle = random.randint(-90, 90)
		halt = random.randint(0,1)

		print ("Angle:", angle, "Halt:", halt)	
		
		# if halt signal is not inferred run direction signalling, else run halt signalling
		if halt <= 0.5:
			# Direction signal involves turning on the buzzer that corresponds to the direction that the user is supposed to go to and continously vibrating it until the user has moved to the right angle
			if angle%2==0:
				GPIO.output(right_buzzer, 1)	
			else:
				GPIO.output(left_buzzer, 1)	
				
			n = angle/(-1*angle)
			# If the displaced angle is within E of the predicted angle break the loop
			while abs(angle) >= E:
				"""
				disp_angle = mpu.get_angle_data["z"]
				angle -= disp_angle 
				"""
				angle -= n
				print (n)
				
			GPIO.output(right_buzzer, 0)	
			GPIO.output(left_buzzer, 0)

		else:
			# Stop signal for 3 seconds
			start_time = time.time()
			GPIO.output(right_buzzer, 1)	
			GPIO.output(left_buzzer, 1)

			time.sleep(3)

			GPIO.output(right_buzzer, 0)	
			GPIO.output(left_buzzer, 0)

if __name__ == "__main__":
	initialize()
	guide_system_run()
