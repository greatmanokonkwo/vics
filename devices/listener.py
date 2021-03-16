"""
This script collects the specified class data in time chunks defined by the user and saves it in a specified path
"""
import pyaudio
import wave

class Listener:
	
	def __init__(self, seconds):
		self.chunk = 1024
		self.FORMAT = pyaudio.paInt16
		self.channels = 1
		self.sample_rate = 8000
		self.record_seconds = seconds

		self.p = pyaudio.PyAudio()
		
		self.stream = self.p.open(format=self.FORMAT,
						channels=self.channels,
						rate=self.sample_rate,
						input=True,
						output=True,
						frames_per_buffer=self.chunk)

	def save_audio(self, file_name, frames):
		print(f"saving file to {file_name}")
		self.stream.stop_stream()
		self.stream.close()
	
		self.p.terminate()
		
		# save audio file
		# open the file in "write bytes" mode
		wf = wave.open(file_name, "wb")
		# set the channels
		wf.setnchannels(self.channels)
		# set the sample format
		wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
		# set the sample rate
		wf.setframerate(self.sample_rate)
		# write the frames as bytes
		wf.writeframes(b"".join(frames))
		# close the file
		wf.close()
