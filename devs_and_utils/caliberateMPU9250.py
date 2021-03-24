import smbus
import numpy as np

from imusensor.MPU9250 import MPU9250

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()

calib_file = "./calib.json"

print("To caliberate the accelerometer you need to place each axis + and - facing gravitational pull of the earth")
print("Thus it is supposed to be 9.8 m/s, and we caliberate it if we isn't")
print("For example lay the accelorometer flat to get the +z and then flip it get -z. Do this for every axis")
start = input("Press enter to start caliberating Accelerometer: ")
imu.caliberateAccelerometer()
print ("Acceleration caliberation successful")

print("To caliberate the magnetometer you need to move it in a figure 8 motion. Make sure you get all the roll and pitch angles.")
start = input("Press enter to start caliberating Magnetometer: ")
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
