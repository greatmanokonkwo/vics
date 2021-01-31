import os
import sys
import time
import smbus
import numpy as np

from imusensor.MPU9250 import MPU9250
from imusensor.filters import madgwick

sensorfusion = madgwick.Madgwick(0.5)

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()

calib_file = "/home/greatman/code/vics/devices/calib.json"

imu.loadCalibDataFromFile(calib_file)	

count = 0
currTime = time.time()

time_cnt = 0

start_time = time.time()
initial_yaw = 0

# Sensor fusion testing for getting angles
"""
init_accel = imu.AccelVals[1]
while True:

	imu.readSensor()
	for i in range(10):
		imu.computeOrientation()
		newTime = time.time()
		dt = newTime - currTime
		currTime = newTime

		sensorfusion.updateRollPitchYaw(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2], imu.GyroVals[0], imu.GyroVals[1], imu.GyroVals[2], imu.MagVals[0], imu.MagVals[1], imu.MagVals[2], dt)

	if time.time()- start_time < 10:
		initial_yaw = sensorfusion.yaw	

	if time_cnt == 2:
		time_cnt = 0	
		#print(f"Accelorometer: {imu.AccelVals[0]} {imu.AccelVals[1]} {imu.AccelVals[2]}")
		#print(f"Gyroscope: {imu.GyroVals[0]} {imu.GyroVals[1]} {imu.GyroVals[2]}")
		#print(f"Magnetometer: {imu.MagVals[0]} {imu.MagVals[1]} {imu.MagVals[2]}")
		#print (f"Roll: {int(sensorfusion.roll)} ; Pitch : {int(sensorfusion.pitch)} ; Yaw : {int(sensorfusion.yaw)}")
		#desired_yaw = int(-(sensorfusion.yaw - initial_yaw))
		#print(f"Desired Yaw: {desired_yaw} ; Initial Yaw: {initial_yaw}")

	time_cnt+=1
	time.sleep(0.01)
"""

# Testing for halt determination

sample_count = 0
midline = -9.8
thresh = 0.6
max_val = -999

currTime = time.time()
while True:
	imu.readSensor()
	
	sample = imu.AccelVals[2]
	max_val = max(max_val, sample)

	newTime = time.time()

	if newTime - currTime >= 1:
		if (max_val - midline) > thresh:
			print(max_val, 0)
		else:
			print(max_val, 1)
	
		max_val = -999

		currTime = newTime
