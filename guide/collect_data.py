# Add vics directory to sys path to have access to devices module
import os
os.sys.path.append("..")

import time
import smbus

from imusensor.MPU9250 import MPU9250
from imusensor.filters import madgwick

from devices.picam import picam

# MPU9250 IMU sensor and sensorfusion algorithm
sensorfusion = madgwick.Madgwick()
imu = None 

# Raspberry Pi Camera V2
cam = None

initial_yaw = 0
prevTime_yaw = None
prevTime_vel = None
y_vel = 0

def initialize_devices(width=256, height=256):
	global imu
	global cam

	cam = picam(width, height)

	# Initialize MPU-6050 device
	address = 0x68
	bus = smbus.SMBus(1)
	imu = MPU9250.MPU9250(bus, address)
	imu.begin()
	
	calib_file = "../devices/calib.json" # path of caliberation file with caliberated values

	if os.path.exists(calib_file):	
		imu.loadCalibDataFromFile(calib_file)

# Check if moving body has halted by approximating the velocity of the moving body using acceloremter values in the y-axis direction
def get_halt_signal():
	global prevTime_vel, y_vel

	# calculate velocity in the y direction by integrating the accelerometer values
	newTime = time.time()
	dt = newTime - prevTime_vel
	prevTime_vel = newTime
	currAccel = imu.AccelVals[1]
	
	y_vel += (currAccel * dt)

	print(currAccel*dt)
	if int(y_vel) == 0:
		return 1
	else:
		return 0
	

# Classify a given angle in degrees as one of the 9 direction classes
# [-PI/2, -3PI/8, -PI/4, -PI/8, 0, PI/8, PI/4, 3PI/8, PI/2]
def get_direction_class(angle):
	if (angle < -78.75) & (angle >= -101.25):
		return 0
	elif (angle < -56.25) & (angle >= -78.75):
		return 1
	elif (angle < -33.75) & (angle >= -56.25):
		return 2
	elif (angle < -11.25) & (angle >= -33.75):
		return 3
	elif (angle < 11.25) & (angle >= -11.25):
		return 4
	elif (angle < 33.75) & (angle >= 11.25):
		return 5
	elif (angle < 56.25) & (angle >= 33.75):
		return 6
	elif (angle < 78.75) & (angle >= 56.25):
		return 7
	elif (angle <= 101.25) & (angle >= 78.75):
		return 8
		
def calculate_yaw():
	global prevTime_yaw

	# Calculate the change in the yaw angle of the mpu9250 device
	imu.readSensor()
	for i in range(10):
		imu.computeOrientation()
		newTime = time.time()
		dt = newTime - prevTime_yaw
		prevTime_yaw = newTime

		sensorfusion.updateRollPitchYaw(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2], imu.GyroVals[0], imu.GyroVals[1], imu.GyroVals[2], imu.MagVals[0], imu.MagVals[1], imu.MagVals[2], dt)

# Data collection process	
def data_collection(mins, path):
	global prevTime_yaw, prevTime_vel

	# Get the ID of the last processed data sample
	with open(path+"/last.txt") as f:
		count = int(f.read())

	START_TIME = time.time()	

	capture_timer = 0 # the below while loop has a frequency of 100 loops per second which is too many pictures to take a second we should should count every 100 loops and take a picture at those points
	prev_yaw = 0
	direct_class = None
	max_angle = 0
	max_halt = 0

	initial_yaw = 0

	img_ = None

	prevTime_yaw = START_TIME
	prevTime_vel = prevTime_yaw

# Loop until specified minutes have elasped
	while time.time() - START_TIME < mins*60:
		
		# Take image at the start of movement interval
		if capture_timer == 0:
			img_ = cam.capture_image()

		# Calculate values for the displacement angle and halt signal
		halt = get_halt_signal()
		max_halt = max(max_halt, halt)

		calculate_yaw()
		#print(sensorfusion.yaw)

		# The sensor fusion algorithm spends the first few seconds of calculations slightly off. In order not the take this off values as are starting values we retake the initial_yaw for the first five seconds
		if time.time() - START_TIME < 5:
			initial_yaw = initial_yaw

		yaw_angle = -(sensorfusion.yaw - initial_yaw) # The magnetometer measures heading from the earth's true north, we need to set the user's initial heading as the reference point
		angle = int(yaw_angle - prev_yaw) # The displacement angle is the (yaw angle) - (previous yaw angle)

		if abs(angle) > abs(max_angle):
			max_angle = angle
				
		# Save the image as well as the motion in format direct_class/id_angle.jpg
		if capture_timer == 100:
			if max_halt:
				direct_class = 9 # Determine the motion class of given the angle and halt signal
			else:
				direct_class = get_direction_class(max_angle)

			#print(max_angle)
			cam.save_image(path=(path+"/"+str(direct_class)+"/"+str(count)+"_"+str(max_angle)+".jpg"), img=img_)
			max_angle = 0
			max_halt = 0
			capture_timer = 0
			prev_yaw = yaw_angle
			count+=1

		capture_timer+=1
		time.sleep(0.01)
			
	# Update the start.txt file with ID of lastest processed data sample
	with open(path+"/last.txt", "w") as f:
		f.write(str(count))

if __name__=="__main__":
	data_path = str(input("Where should the dataset be stored (The path should contain a last.txt file and an images directory):"))
	initialize_devices()
	print ("Get set up. Data collection will start in 30 seconds.")
	time.sleep(0)
	data_collection(mins=2, path=data_path)
	cam.cleanup()
