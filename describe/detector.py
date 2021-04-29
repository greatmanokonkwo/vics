import numpy as np
import argparse
import time
import cv2
import os

class ObjectDetector:
	def __init__(self, confidence=0.4, nms_thresh=0.4):
		self.confidence = confidence
		self.nms_thresh = nms_thresh
		
		# load the COCO class labels our YOLO model was trained on
		labelsPath = "data/coco.names"
		self.LABELS = open(labelsPath).read().strip().split("\n")

		# derive the paths to the YOLO weights and model configuration
		weightsPath = "weights/yolov3-tiny.weights"
		configPath = "cfg/yolov3-tiny.cfg"

		# load our YOLO object detector trained on COCO dataset (80 classes)
		print("[INFO] loading YOLO from disk...")
		self.net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

	def detect(self, image):
		(H, W) = image.shape[:2]
		
		# determine only the *output* layer names that we need from YOLO
		ln = self.net.getLayerNames()
		ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

		# construct a blob from the input image and then perform a forward
		# pass of the YOLO object detector, giving us our bounding boxes and
		# associated probabilities
		blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
			swapRB=True, crop=False)
		self.net.setInput(blob)
		start = time.time()
		layerOutputs = self.net.forward(ln)
		end = time.time()

		# show timing information on YOLO
		print("[INFO] YOLO took {:.6f} seconds".format(end - start))		

		# initialize our lists of detected bounding boxes, confidences, and
		# class IDs, respectively
		boxes = []
		confidences = []
		classIDs = []

		# loop over each of the layer outputs
		for output in layerOutputs:
			# loop over each of the detections
			for detection in output:
				# extract the class ID and confidence (i.e., probability) of
				# the current object detection
				scores = detection[5:]
				classID = np.argmax(scores)
				confidence = scores[classID]
				# filter out weak predictions by ensuring the detected
				# probability is greater than the minimum probability
				if confidence > self.confidence:
					# scale the bounding box coordinates back relative to the
					# size of the image, keeping in mind that YOLO actually
					# returns the center (x, y)-coordinates of the bounding
					# box followed by the boxes' width and height
					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")
					# use the center (x, y)-coordinates to derive the top and
					# and left corner of the bounding box
					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))
					# update our list of bounding box coordinates, confidences,
					# and class IDs
					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					classIDs.append(classID)

		# apply non-maxima suppression to suppress weak, overlapping bounding
		# boxes
		idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence,
			self.nms_thresh)	

		res = []

		# ensure at least one detection exists
		if len(idxs) > 0:
			# loop over the indexes we are keeping
			for i in idxs.flatten():
				# extract the bounding box coordinates
				(x, y) = (boxes[i][0], boxes[i][1])
				(w, h) = (boxes[i][2], boxes[i][3])

				# extract the bounding box coordinates and labels
				res.append([x, y, x+w, y+h, self.LABELS[classIDs[i]]])
		
		return res	

if __name__=="__main__":
	detector = ObjectDetector()
	img = cv2.imread(input("Path of test input image: "))
	print(detector.detect(img))

