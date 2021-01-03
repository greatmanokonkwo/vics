import time
import smbus
import math

from imusensor.MPU9250 import MPU9250
from imusensor.filters import madgwick

from vics.tools_and_devices.picam import picam

# MPU9250 IMU sensor and sensorfusion algorithm
sensorfusion - madgwick.Madgwick(0.5)
imu = None 

# Raspberry Pi Camera V2
cam = None

def initialize_devices(width=256, height=256):
	global imu
	global cam

	# Initialize MPU-6050 device
	address = 0x68
	bus = smbus.SMBus(1)
	imu = MPU9250.MPU9250(bus, address)
	imu.begin()

	# Calibrate IMU sensor
	imu.caliberateGyro()
	imu.caliberateAccelerometer()
	imu.caliberateMagPrecise()

	cam = picam(width, height)

def get_halt_signal(accel):
	# The halt signal will be ON if a large negative value in the x-direction is calculated

	if abs(accel) > 10 and accel%2!=0:
		return "halt"
	else: 
		return "no_halt"

# Data collection process	
def data_collection(mins, path):
	
	# Get the ID of the last processed data sample
	with open(path+"/last.txt") as f:
		count = int(f.read())

	start_time = time.time()	
	
	count = 0	
	prev_yaw = 0
	# Loop until specified minutes have elasped
	while time.time() - start_time < mins*60:
		count+=1	
		# Getting smooth readings from the IMU sensor
		imu.readSensor()
		for	i in range(10):
			newTime = time.time()
			dt = newTime - currTime
			currTime = newTime
		
			sensorfusion.updateRollPitchYaw(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2], imu.GyroVals[0],
									imu.GyroVals[1], imu.GyroVals[2], imu.MagVals[0], imu.MagVals[1], imu.MagVals[2], dt)
	
		
		# Capture and save image and save the values of the angle and halt signal
		halt = get_halt_signal(imu.AccelVals[1])
		angle = (math.radians(sensorfusion.yaw - prev_yaw))
		cam.save_image(path+"/"+str(halt_path)+"/"+str(count)+"_"+str(angle)+".jpg")
		prev_yaw = sensorfusion.yaw
		time.sleep(0.1)
			
	# Update the start.txt file with ID of lastest processed data sample
	with open(path+"/last.txt", "w") as f:
		f.write(str(count))

data_path = str(input("Where should the dataset be stored (The path should contain a last.txt file and an images directory):"))
initialize_devices()
time.sleep(30)
data_collection(mins=1, path=data_path)
cam.cleanup()
