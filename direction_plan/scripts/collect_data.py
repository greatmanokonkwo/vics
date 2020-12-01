from tauras_silver.devices import *
from picamera import PiCamera
import time

# MPU-6050 Gyroscope and Accelorometer
mpu = mpu6050(0x68)

# Raspberry Pi Camera V2
picam = PiCamera()

def initialize_devices(preview=True):
	# Initialize MPU-6050 device
	mpu.set_accel_range(mpu.ACCEL_RANGE_2G)
	mpu.set_gryo_range(mpu.GYRO_RANGE_2000DEG)
	mpu.gyro_calibrate()
	
	#Show camera preview
	if (preview):
		picam.show_preview()
		time.sleep(5)
		picam.stop_preview()

def get_halt_signal(accel):
	# The halt signal will be ON if a large negative value in the x-direction is calculated

	if abs(accel) > C && accel%2!=0:
		return 1
	else: 
		return 0
	
# Data collection process	
def data_collection(mins):
	
	# Get the ID of the last processed data sample
	with open("../../dataset/last.txt") as f:
		count = f.read()

	start_time = time.time()	
	
	angle_halt = open("../../dataset/angle_halt.txt", "a")	

	max_angle = 0
	max_accel = 0
	
	segment_start = time.time()
	# Loop until specified minutes have elasped
	while time.time() - start_time < mins*60:
		angle = mpu.get_angle_data()['z']
		accel = mpu.get_accel_data()['x']
		
		if abs(angle) > abs(max_angle):
			max_angle = angle
	
		if abs(accel) > abs(max_accel):
			max_accel = accel
	
		if time.time() - segment_start > 1:
			count+=1
			# Capture and save image
			picam.capture("../../dataset/images/"+count+".jpg")

			halt = get_halt_signal(max_accel)
			
			# write the calculated values of the angle and the halt signal to the angle_halt.txt file	
			print(max_angle+" "+max_accel+"\n")
			angle_halt.write(max_angle+" "+max_accel+"\n")		

			max_angle = 0
			max_accel = 0

			segment_start = time.time()	

	angle_halt.close()

	# Update the start.txt file with ID of lastest processed data sample
	with open("../../dataset/last.txt", "w") as f:
		f.write(count) 

if __name__ == "__main__":
	initialize_devices()
	data_collection(fps=1,mins=1)
