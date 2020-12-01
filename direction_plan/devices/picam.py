import cv2

class picam:
	cam = None
	
	def __init__(self, width, height):
		self.cam = cv2.VideoCapture(self.gstreamer_pipeline(width, height), cv2.CAP_GSTREAMER)
	
	def gstreamer_pipeline(self, capture_width=256, capture_height=256, framerate=60):
		return (
			"nvarguscamerasrc ! "
			"video/x-raw(memory:NVMM), "
			"width=(int)%d, height=(int)%d, "
			"format=(string)NV12, framerate=(fraction)%d/1 ! "
			"nvvidconv flip-method=0 ! "
			"video/x-raw, width=(int)1280, height=(int)720, format=(string)BGRx ! "
			"videoconvert ! "
			"video/x-raw, format=(string)BGR ! appsink"
			% (
				capture_width,
				capture_height,
				framerate
			)
		)

	def save_image(self, path):
		if self.cam.isOpened():
			ret_val, img = self.cam.read()
			cv2.imwrite(path, img)
		else:
			print("Unable to open camera")

	def cleanup(self):
		self.cam.release()
