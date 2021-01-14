import os
import sys
import time
import smbus
import numpy as np

from imusensor.MPU9250 import MPU9250
from imusensor.filters import kalman

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()

calib_file = "/home/greatman/code/vics/devices/calib.json"
	
caliberate = str(input("Do you want to caliberate the sensor: "))

if caliberate.lower() == "yes":
	imu.caliberateAccelerometer()
	print ("Acceleration caliberation successful")
	imu.caliberateMagPrecise()
	print ("Magnetometer caliberation successful")

	accelscale = imu.Accels
	accelBias = imu.AccelBias
	gyroBias = imu.GyroBias
	mags = imu.Mags 
	magBias = imu.MagBias

	imu.saveCalibDataToFile(calib_file)
	print ("calib data saved")

	imu.loadCalibDataFromFile(calib_file)
	if np.array_equal(accelscale, imu.Accels) & np.array_equal(accelBias, imu.AccelBias) & \
		np.array_equal(mags, imu.Mags) & np.array_equal(magBias, imu.MagBias) & \
		np.array_equal(gyroBias, imu.GyroBias):
		print ("calib loaded properly")
else:
	if os.path.exists(calib_file):
		imu.loadCalibDataFromFile(calib_file)	

sensorfusion = kalman.Kalman()

imu.readSensor()
imu.computeOrientation()

sensorfusion.roll = imu.roll
sensorfusion.pitch = imu.pitch
sensorfusion.yaw = imu.yaw

count = 0
currTime = time.time()

time_cnt = 0
while True:
	time_cnt+=1

	imu.readSensor()
	imu.computeOrientation()
	newTime = time.time()
	dt = newTime - currTime
	currTime = newTime

	sensorfusion.computeAndUpdateRollPitchYaw(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2], imu.GyroVals[0], imu.GyroVals[1], imu.GyroVals[2], imu.MagVals[0], imu.MagVals[1], imu.MagVals[2], dt)

	time.sleep(0.01)
	
	if time_cnt == 100:
		time_cnt = 0	
		print ("roll: {0} ; pitch : {1} ; yaw : {2}".format(sensorfusion.roll, sensorfusion.pitch, sensorfusion.yaw))
		print ("")
