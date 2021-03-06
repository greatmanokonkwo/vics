"""
BEFORE RUNNING DATA_COLLECTION SCRIPT MAKE SURE THE MPU9250 HAS BEEN PROPERLY CALIBERATED AND PRODUCEDS ACCURATE YAW VALUES

SPEED CONSIDERATIONS:
- Walk at an average pace of 0.5 m/s or anything around there. 
- If you need to walker faster/slower then you would need to change to update time of the collector
- The collector runs at an update time of approx 1 second (collects image and direction pairs)
- Modify the UPDATE_TIME constant just on the top of the file. The wearter can test out direction UPDATE_TIME values for optimal usage

ROTATIONS:
- Rotations are calculated as the maximum displacement angle within the UPDATE_TIME span
- That being said the wearer should be certain of the direction they want to go. Make dilberate turns
- DON'T TURN MORE THAN 90 DEGREES IN EACH DIRECTION! The system only considers angles within [-101.25, 101.25] degrees (202.25 degrees) 
- Rotations should also be done in the window of the update time 

STOPPING:
- The stopping detector works by keep track of the bouncing motion on the z-axis. 
- Since while walking the user moves up and down and algorithm knows the user has stopped walking when the up and down motion stops
- The up and down motion is detected using the accelerometer sensors z-axis
- At rest the value of the accelerometer's z-axis is -9.8 meters, representing the acceleration due to gravity
- The algorithm calculates the accelerometer values over the spand of UPDATE_TIME and saves the maximum value over that interval
- Then, if the difference betwee n the maximum acceleration value and the rest value is greater than some threshold value THRESH, it is concluding that user is walking
- The value of THRESH can be tweaked to match the walking style of the user.

TESTING:
- For testing the angle, halt and final direction class values are printed out to the standard output
- Looking at these values can help tweak some of the values like UPDATE_TIME and THRESH
- For more testing on the mpu9250 yaw estimation and halt detection, go to ../devices/test_mpu.py

STOPPING CONDITIONS:
- Stop when a human being is in front of you
- Stop in front of a crosswalk
- Stop when there is a closed door in front of you in a closed room, open in the door and continue. Whiling opeing door, try not to make a lot of movements
- Stop when stairs have been encountered. Try to get top and bottom views of stairs in data. Same goes for escalators if any encountered. Highly doubt though

WHAT TO DO:
- Walk down multiple routes like you would normally do
- Try to capture edge cases such as environments with glass doors, stairs, and crosswalks from direction viewing angles, while walking
""" 

import os
os.sys.path.append("..")

import cv2
import time
import smbus

from imusensor.MPU9250 import MPU9250
from imusensor.filters import madgwick

from devs_and_utils.picam import picam 

# UPDATE TIMER VARAIBLE
UPDATE_TIME = 2.8
MIDLINE = -9.8
THRESH = 0.6

# MPU9250 IMU sensor and sensorfusion algorithm
sensorfusion = madgwick.Madgwick()
imu = None 

# Raspberry Pi Camera V2
cam = None 

capture_type = None # The script can either collect image data from live camera feed or prerecorded and saved video data

initial_yaw = 0

def initialize_devices(width=256, height=256):
	global imu

	if capture_type == "live":
		global cam 
		cam = picam(width, height)
	
	# Initialize MPU-6050 device
	address = 0x68
	bus = smbus.SMBus(1)
	imu = MPU9250.MPU9250(bus, address)
	imu.begin()
	
	calib_file = "../devs_and_utils/calib.json" # path of caliberation file with caliberated values

	if os.path.exists(calib_file):	
		imu.loadCalibDataFromFile(calib_file)
	else:
		print("Unable to find IMU caliberation file")

# Classify a given angle in degrees as one of the 9 direction classes
# [-PI/2, -3PI/8, -PI/4, -PI/8, 0, PI/8, PI/4, 3PI/8, PI/2]
def get_direction_class(angle):
	if (angle < -67.5) & (angle >= -112.5):
		return 0
	elif (angle < -22.5) & (angle >= -67.5):
		return 1
	elif (angle < 22.5) & (angle >= -22.5):
		return 2
	elif (angle < 67.5) & (angle >= 22.5):
		return 3
	elif (angle < 112.5) & (angle >= 67.5):
		return 4
	else:
		return -1
		
def calculate_yaw(currTime):
	
	# Calculate the change in the yaw angle of the mpu9250 device
	for i in range(10):
		newTime = time.time()
		dt = newTime - currTime
		currTime = newTime

		sensorfusion.updateRollPitchYaw(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2], imu.GyroVals[0], imu.GyroVals[1], imu.GyroVals[2], imu.MagVals[0], imu.MagVals[1], imu.MagVals[2], dt)
	
	return currTime

# Data collection process	
def data_collection(mins, path, fps, sample):
	global prevTime_yaw, prevTime_vel

	# Creating a VideoCapture object to read the video
	cap = cv2.VideoCapture(sample)

	# Get the ID of the last processed data sample
	with open(path+"/last.txt") as f:
		count = int(f.read())

	START_TIME = time.time()	

	img = None

	# Yaw calculation variables
	prev_yaw = 0
	direct_class = None
	max_angle = 0
	initial_yaw = 0

	# Halt classification variables
	## Halting is classified by using the principle that when people walk they oscillate up and down. Given the acceleration in the z-axis we can thus determine if the user is walking by calculating the amplitude value at a given interval. If the amplitude is below a certain threshold that means the user is not walking
	midline = -9.8
	thresh = 0.6
	max_accel = -999	

	currTime = time.time()

	# Loop until specified minutes have elasped

	if capture_type == "live":
		
		interval_start = START_TIME
		new_interval = True

		while time.time() - START_TIME < mins*60:

			imu.readSensor()
			currTime = calculate_yaw(currTime)

			newTime = time.time()

			# The sensor fusion algorithm spends the first few seconds of calculations slightly off. In order not the take this off values as are starting values we retake the initial_yaw for the first five seconds
			if newTime - START_TIME < 12.5:
				initial_yaw = sensorfusion.yaw
				interval_start = newTime
				continue
			
			# Take a frame from each second of the video
			if new_interval:
				new_interval = False
				img = cam.capture_image()
				
			# Calculate maximum accelorometer value on the z-axis
			max_accel = max(imu.AccelVals[2], max_accel)

			yaw_angle = -(sensorfusion.yaw - initial_yaw) # The magnetometer measures heading from the earth's true north, we need to set the user's initial heading as the reference point
			angle = int(yaw_angle - prev_yaw) # The displacement angle is the (yaw angle) - (previous yaw angle)

			if abs(angle) > abs(max_angle):
				max_angle = angle
				
			# Save he image as well as the motion in format direct_class/id_angle.jpg
			if newTime - interval_start >= UPDATE_TIME:

				halt = 0
				if (max_accel - MIDLINE) < THRESH:
					direct_class = 5 # Halt was detected
					halt = 1
				else:
					direct_class = get_direction_class(max_angle)

				if direct_class != -1:
					# Save image and direction pair
					cam.save_image(path=(path+"/"+str(direct_class)+"/"+str(count)+"_"+str(max_angle)+".jpg"), img=img)
								
					# Test out the angle, stop and direction class values. For max_accel if you are walking it should be 0 and if you stop it should be 1
					print(max_angle, halt, direct_class, yaw_angle, prev_yaw)
				else:
					print("Invalid movement direction")

				max_angle = 0
				max_halt = 0
				prev_yaw = -(sensorfusion.yaw - initial_yaw)
	
				max_accel = -999
			
				interval_start = time.time()
				new_interval = True

				count+=1

	else:	
	
		fps_counter = 0

		while (cap.isOpened()):

			imu.readSensor()
			currTime = calculate_yaw(currTime)

			# The sensor fusion algorithm spends the first few seconds of calculations slightly off. In order not the take this off values as are starting values we retake the initial_yaw for the first five seconds
			if time.time() - START_TIME < 12.5:
				initial_yaw = sensorfusion.yaw
				continue

			# Collect a frame each time in the loop	
			ret, frame = cap.read()
			cv2.imshow("Video", frame)
		
			# Calculate maximum accelorometer value on the z-axis
			max_accel = max(imu.AccelVals[2], max_accel)

			yaw_angle = -(sensorfusion.yaw - initial_yaw) # The magnetometer measures heading from the earth's true north, we need to set the user's initial heading as the reference point
			angle = int(yaw_angle - prev_yaw) # The displacement angle is the (yaw angle) - (previous yaw angle)

			if abs(angle) > abs(max_angle):
				max_angle = angle
				
			# Save he image as well as the motion in format direct_class/id_angle.jpg
			if fps_counter >= fps:
				fps_counter = 0
				img = cv2.resize(frame, (416, 416), fx=0, fy=0, interpolation = cv2.INTER_CUBIC)

				halt = 0
				if (max_accel - MIDLINE) < THRESH:
					direct_class = 9 # Halt was detected
					halt = 1
				else:
					direct_class = get_direction_class(max_angle)

				if direct_class != -1:
					# Save image and direction pair
					cv2.imwrite((path+"/"+str(direct_class)+"/"+str(count)+"_"+str(max_angle)+".jpg"), img)
								
					# Test out the angle, stop and direction class values. For max_accel if you are walking it should be 0 and if you stop it should be 1
					print(max_angle, halt, direct_class)
				else:
					print("Invalid movement direction")

				max_angle = 0
				max_halt = 0
				prev_yaw = -(sensorfusion.yaw - initial_yaw)
	
				max_accel = -999
			
				count+=1

	# Update the start.txt file with ID of lastest processed data sample
	with open(path+"/last.txt", "w") as f:
		f.write(str(count))

if __name__=="__main__":
	data_path = str(input("Where should the dataset be stored (The path should contain a last.txt file and an images directory): "))
	capture_type = str(input("Is the data coming from a live camera feed or a prerecorded video? (live or video): ")).lower()

	mins = None
	fps = None
	video_sample = None

	if capture_type == "live":
		mins = float(input("How long should the collection script run (in mins): "))
	else:
		video_sample = str(input("Path of your video data sample: "))
		fps = int(input("What is the fps of the video? "))
	
	initialize_devices()

	print ("Get set up. Data collection will start in 30 seconds.")
	# Give time handle any setups to get collector ready to start taking in data
	# time.sleep(30)
	# Change the minutes to the how long you want to run the program for 
	data_collection(mins=mins, path=data_path, fps=fps, sample=video_sample)

	if capture_type == "live":
		cam.cleanup()
