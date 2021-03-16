"""
This script collects the specified class data in time chunks defined by the user and saves it in a specified path
"""
import os.sys
sys.path.append("..")

import pyaudio
import wave
import time
import os

from devices.listener import Listener

def record(seconds, save_path):
	index = 0
	try:
		while True:
			listener = Listener(seconds)
			frames = []
			
			print("begin recording...")
			input(f"press enter to continue. The recording will be {} seconds. press ctrl + c to exit")
			time.sleep(0.2)
			for i in range(int((listener.sample_rate/listener.chunk) * listener.record_seconds)):
				data.
	
if __main__=="__name__":
	data_class = input("Which data class do you want to train. 0 - Other speech, 1 - Guide me, 2 - Read this, 3 - Describe the scene: ")
	save_path = input("Where should the file by saved: ")
	secs = int(input("How many seconds should each recording chunk be?: ")

	record(secs, save_path)
