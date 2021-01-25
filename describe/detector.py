import cv2
from darknet import Darknet
from util import *
from torch.autograd import Variable
import torch

class ObjectDetector:
	def __init__(self, confidence=0.5, nms_thresh=0.4, reso=416):
		
		#Load Darknet model for object detection
		print("Loading network...")
		self.model = Darknet("cfg/yolov4-tiny.cfg")
		self.model.load_weights("yolov4-tiny.weights")
		print("Network successfully loaded")

		self.model.net_info["height"] = reso
		self.inp_dim = int(self.model.net_info["height"])
		if torch.cuda.is_available():
			self.model.cuda()

		self.model.eval()

		#Set detector parameters
		self.confidence = confidence
		self.nms_thresh = nms_thresh
		self.reso = reso

		#Load class file
		self.num_classes = 80
		self.classes = load_classes("data/coco.names")

	def detect(self, img):
		img_ = prep_image(img, self.inp_dim)
	
		if torch.cuda.is_available():
			img_.cuda()

		pred = self.model(img_, torch.cuda.is_available())
		res = write_results(pred, self.confidence, self.num_classes)[:,[1,2,3,4,7]] # only take the 4 corner coordinate points and class index
	
		# Create a python list for all the objects with the format [x1,y1,x2,y2,class_name]
		objs = []
		for obj in res:
			_ = obj[:4].tolist()
			_.append(self.classes[int(obj[4])])
			objs.append(_)

		return objs

if __name__=="__main__":
	detector = ObjectDetector()
	img = cv2.imread(input("Input image path: "))
	print(detector.detect(img))
