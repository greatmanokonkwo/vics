import cv2
import PIL import Image
import pytresseract

class ReadingSystem:
	def __init__(self, width=416, height=416):
		# Ras[berry Pi Camfor taking 416x416 images of scenery
		self.cam = picam(width=width, height=height)
	
		# If you don't have tesseract executable in your PATH, include the following:	
		self.pytesseract.pytesseract.tesseract_cmd = r"<fall_path_to_your_tesseract-executable>"

	def run(self):		
		img = self.cam.capture_image()
		img_ = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img_ = Image.fromarray(img) # convert opencv image to PIL

		response = self.pytesseract.image_to_string(img_)
		print(response)

if __name__=="__main__":
	system = ReadingSystem()
	system.run()
