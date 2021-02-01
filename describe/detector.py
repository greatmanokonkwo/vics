import cv2
from tool.darknet2pytorch import Darknet
from utils.utils import *
import torch.cuda

class ObjectDetector:
	def __init__(self, cfgfile, weightfile, confidence=0.5, nms_thresh=0.4, reso=416):
		
		#Load Darknet model for object detection
		self.model = Darknet(cfgfile)
		self.model.print_network()
		self.model.load_weights(weightfile)
		print(f"Loading weights from {weightfile}... Done!")

		self.CUDA = torch.cuda.is_available()

		if self.CUDA:
			self.model.cuda()

		#Set detector parameters
		self.confidence = confidence
		self.nms_thresh = nms_thresh
		self.reso = reso

		#Load class file
		self.num_classes = 80
		self.classes = load_class_names("data/coco.names")

	def detect(self, img):
		img_ = cv2.resize(img, (self.model.width, self.model.height))
		img_ = cv2.cvtColor(img_, cv2.COLOR_BGR2RGB)
	
		if self.CUDA:
			img_ = img_.cuda()

		boxes = do_detect(self.model, img_, self.confidence, self.nms_thresh, self.CUDA)
		print(boxes)
		
		"""
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
		"""
	
if __name__=="__main__":
	detector = ObjectDetector("cfg/yolov3.cfg", "yolov3.weights")
	img = cv2.imread(input("Input image path: "))
	print(detector.detect(img))
