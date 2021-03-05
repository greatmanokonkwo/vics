from os import sys
sys.path.append("..")

import cv2
from PIL import Image
import pytesseract

from devices.picam import picam

class ReadingSystem:
	def __init__(self, width=416, height=416):
		# Raspberry Pi Camfor taking 416x416 images of scenery
		self.cam = picam(width=width, height=height)
	
		# If you don't have tesseract executable in your PATH, include the following:	
		pytesseract.pytesseract.tesseract_cmd = r"<fall_path_to_your_tesseract-executable>"

	def run(self):		
		#img = self.cam.capture_image()
		img = cv2.imread("test.png")	
		img_ = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		response = pytesseract.image_to_string(img_)
		print(response)

if __name__=="__main__":
	system = ReadingSystem()
	system.run()
