import os
os.sys.path.append("..")

import cv2
import pytesseract

from devices.picam import picam
from devices.google_voice import GoogleVoice

from playsound import playsound

class ReadingSystem:
	def __init__(self, width=416, height=416):
		# Raspberry Pi Camfor taking 416x416 images of scenery
		self.cam = picam(width=width, height=height)
		self.voice = GoogleVoice()
	
		# If you don't have tesseract executable in your PATH, include the following:	
		pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

	def run(self):		
		#img = self.cam.capture_image()
		img = cv2.imread("test.jpg")
		img_ = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		response = pytesseract.image_to_string(img_)
		self.voice.text_to_speech(voice_name="en-GB-Standard-B", text=response, name="response")
	
		print(response)
		playsound("response.wav")
		os.remove("response.wav")

	def cleanup(self):
		self.cam.cleanup()

if __name__=="__main__":
	system = ReadingSystem()
	system.run()
	system.cleanup()	
