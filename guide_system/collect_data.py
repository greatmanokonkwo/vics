import time
import smbus
import math

from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

from vics.tools_and_devices.picam import picam

# MPU9250 IMU sensor and sensorfusion algorithm
sensorfusion = madgwick.Madgwick(0.5)
imu = None 

# Raspberry Pi Camera V2
cam = None

def initialize_devices(width=256, height=256):
	global imu
	global cam

	cam = picam(width, height)

	# Initialize MPU-6050 device
	imu = MPU9250(
    	address_ak=AK8963_ADDRESS, 
    	address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    	address_mpu_slave=None, 
    	bus=1,
    	gfs=GFS_1000, 
    	afs=AFS_8G, 
    	mfs=AK8963_BIT_16, 
    	mode=AK8963_MODE_C100HZ)

	#Calibrate IMU sensor
	imu.calibrate()
	imu.configure()

# TODO: Implement yaw angle calculations
def get_yaw_angle():

def get_halt_signal(accel):
	# The halt signal will be ON if a large negative value in the x-direction is calculated
	if abs(accel) > 10 and accel%2!=0:
		return 1
	else: 
		return 0

# Classify a given angle in degrees as one of the 9 direction classes
# [-PI/2, -3PI/8, -PI/4, -PI/8, 0, PI/8, PI/4, 3PI/8, PI/2]
def get_direction_class(angle):
	if angle > -78.75 && angle <= -101.25:
		return 0
	elif angle > -56.25 && angle <= -78.75:
		return 1
	elif angle > -33.75 && angle <= -56.25:
		return 2
	elif angle > -11.25 && angle <= -33.75:
		return 3
	elif angle > 11.25 && angle <= -11.25:
		return 4
	elif angle > 33.75 && angle <= 11.25:
		return 5
	elif angle > 56.25 && angle <= 33.75:
		return 6
	elif angle > 78.75 && angle <= 56.25:
		return 7
	elif angle >= 101.25 && angle <= 78.75:
		return 8
		
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
		# Calculate values for the displacement angle and halt signal
		halt = get_halt_signal(imu.AccelVals[1])
		angle = get_yaw_angle()

		# Determine the motion class of given the angle and halt signal
		direct_class = None
		if halt:
			direct_class = 9
		else:
			direct_class = get_direction_class(angle - prev_angle)

		# Save the image as well as the motion in format direct_class/id_angle.jpg
		cam.save_image(path+"/"+str(direct_class)+"/"+str(count)+"_"+str(angle - prev_angle)+".jpg")

		prev_angle = angle
		time.sleep(0.1)
			
	# Update the start.txt file with ID of lastest processed data sample
	with open(path+"/last.txt", "w") as f:
		f.write(str(count))

if __name__=="__main__":
	data_path = str(input("Where should the dataset be stored (The path should contain a last.txt file and an images directory):"))
	initialize_devices()
	time.sleep(30)
	data_collection(mins=1, path=data_path)
	cam.cleanup()
