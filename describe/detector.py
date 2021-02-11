import cv2
from darknet import Darknet
from util import *
from torch.autograd import Variable
import torch.cuda

class ObjectDetector:
	def __init__(self, confidence=0.5, nms_thresh=0.4, reso=416):
		
		#Load Darknet model for object detection
		print("Loading network...")
		self.model = Darknet("cfg/yolov3-tiny.cfg")
		self.model.load_weights("weights/yolov3-tiny.weights")
		print("Network successfully loaded")
		
		self.CUDA = torch.cuda.is_available()
		self.model.net_info["height"] = reso
		self.inp_dim = int(self.model.net_info["height"])

		"""
		if self.CUDA:
			self.model.cuda()
		"""

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

		"""
		if self.CUDA:
			img_ = img_.cuda()
			torch.cuda.synchronize() # Wait for GPU to complete inference operations
		"""

		pred = self.model(img_, self.CUDA)
		res = write_results(pred, self.confidence, self.num_classes) # only take the 4 corner coordinate points and class index

		if type(res) != int:
			res = res[:,[1,2,3,4,7]]	
			# Create a python list for all the objects with the format [x1,y1,x2,y2,class_name]

			objs = []
			for obj in res:
				_ = obj[:4].tolist()
				_.append(self.classes[int(obj[4])])
				objs.append(_)

			return objs

		else:
			return res	
		
if __name__=="__main__":
	detector = ObjectDetector()
	img = cv2.imread(input("Path of test input image: "))
	print(detector.detect(img))
