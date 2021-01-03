import time
import smbus
import math

from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
from imusensor.filters import madgwick

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
		currTime = time.time()
		for i in range(10):
			newTime = time.time()
			dt = newTime - currTime
			currTime = newTime
		
			accel = imu.readAccelerometerMaster()
			gyro = imu.readGyroscopeMaster()
			mag = imu.readMagnetometerMaster()

			sensorfusion.updateRollPitchYaw(accel[0], accel[1], accel[2], gyro[0], gyro[1], gyro[2], mag[0], mag[1], mag[2], dt)
	
		# Capture and save image and save the values of the angle and halt signal
		halt = get_halt_signal(imu.AccelVals[1])
		angle = sensorfusion.yaw - prev_yaw
		cam.save_image(path+"/"+str(halt_path)+"/"+str(count)+"_"+str(angle)+".jpg")
		prev_yaw = sensorfusion.yaw
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
