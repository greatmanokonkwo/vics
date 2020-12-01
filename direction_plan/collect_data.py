from devices.mpu6050 import mpu6050
from devices.picam import picam
import time

# MPU-6050 Gyroscope and Accelorometer
mpu = mpu6050(0x68)

# Raspberry Pi Camera V2
cam = picam(width=1000, height=800) 

def initialize_devices():
	# Initialize MPU-6050 device
	mpu.set_accel_range(mpu.ACCEL_RANGE_2G)
	mpu.set_gyro_range(mpu.GYRO_RANGE_2000DEG)
	mpu.gyro_calibrate()
	
def get_halt_signal():
	# The halt signal will be ON if a large negative value in the x-direction is calculated

	accel_x = round(mpu.get_accel_data()['x'])

	if abs(accel_x) > 10 and accel_x%2!=0:
		return 1
	else: 
		return 0
	
# Data collection process	
def data_collection(mins):
	
	# Get the ID of the last processed data sample
	with open("../dataset/last.txt") as f:
		count = int(f.read())

	start_time = time.time()	
	
	angle_halt = open("../dataset/angle_halt.txt", "a")	

	# Loop until specified minutes have elasped
	while time.time() - start_time < mins*60:
		count+=1
	
		# Capture and save image
		cam.save_image("../dataset/images/"+str(count)+".jpg")

		angle = round(mpu.get_angle_data()['z'])
		#halt = get_halt_signal()
		halt = round(mpu.get_accel_data()['x'])
			
		# write the calculated values of the angle and the halt signal to the angle_halt.txt file	
		angle_halt.write(""+str(angle)+" "+str(halt)+"\n")		

	angle_halt.close()

	# Update the start.txt file with ID of lastest processed data sample
	with open("../dataset/last.txt", "w") as f:
		f.write(str(count))

initialize_devices()
print("Data collection starting in 60 seconds...")
time.sleep(60)
print("Recording now")
data_collection(mins=3)
