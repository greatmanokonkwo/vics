"""
Processes the output of the YOLO objection detection algorithm to get a list of object that were found in the image as well as their locations.
The engine then uses a text-to-speech module to say what was in the captured scenery
"""
import cv2
import asyncio

import numpy as np
from detector import ObjectDetector

from playsound import playsound


class SceneDescribeSystem:
	
	def __init__(self, division=1):
		"""Modules"""	
		self.division = division # Use _get_object_location1 or __get_object_location2
		self.scene_size = None

		# object detector
		self.detector = ObjectDetector()

	# Takes information of a box and returns the box location (Top left, Top center, Top right, Bottom left, Bottom center, Bottom right)
	def __get_object_location1(self, x1, y1, x2, y2):
		scene_3 = self.scene_size/3
		scene_2 = self.scene_size/2
		divs_x = [scene_3, 2*scene_3, self.scene_size]
		divs_y = [scene_2, self.scene_size]

		x_overlaps = [0,0,0]
		y_overlaps = [0,0]
	
		for i in range(3):
			overlapx = max(min(x2, divs_x[i]) - max(x1, divs_x[i]-scene_3), 0)
			x_overlaps[i] = overlapx;	

		for i in range(2):
			overlapy = max(min(y2, divs_y[i]) - max(y1, divs_y[i]-scene_2), 0)
			y_overlaps[i] = overlapy;	

		x_div_name = ["left", "center", "right"]
		y_div_name = ["top", "bottom"]
	
		return (y_div_name[np.argmax(np.array(y_overlaps))] + " " + x_div_name[np.argmax(np.array(x_overlaps))])

	# Takes information of a box and returns the box location (Top left, Top center, Top right, Mid left, Mid center, Mid right, Bottom left, Bottom center, Bottom right)
	def __get_object_location2(self, x1, y1, x2, y2):
		scene_3 = self.scene_size/3
		divs = [scene_3, 2*scene_3, self.scene_size]

		x_overlaps = [0,0,0]
		y_overlaps = [0,0,0]
	
		for i in range(3):
			overlapx = max(min(x2, divs[i]) - max(x1, divs[i]-scene_3), 0)
			x_overlaps[i] = overlapx;	

			overlapy = max(min(y2, divs[i]) - max(y1, divs[i]-scene_3), 0)
			y_overlaps[i] = overlapy;	

		x_div_name = ["left", "center", "right"]
		y_div_name = ["top", "mid", "bottom"]
	
		return (y_div_name[np.argmax(np.array(y_overlaps))] + " " + x_div_name[np.argmax(np.array(x_overlaps))])


	# Take in a list of objects detected in scene and return an appropriate text response that describes the scene
	def __generate_response(self, objs):
		response = ""

		for key in objs:
			locs = objs[key]
			n = len(locs)

			if n > 1:
				key_str = f"There are {n} {key}s in the scene "
			else:
				key_str = f"There is one {key} in the scene at the {locs[0]}. "
				response += key_str
				continue
			
			for i in range(n):
				if i == n-1 and n > 1:
					key_str += "and "
				key_str += f"one at the {locs[i]} "
		
			key_str += ". "
			response += (key_str)
		
		return response

	def run(self, cam):
		# Capture the scene and returned voice response of the objects in the scene def run(self, division=2): # Capture image
		#img = cam.capture_image()
		img = cv2.imread("imgs/1.jpg")
		(H, W) = img.shape[:2]
		self.scene_size = W	
	
		# Run inference
		res = self.detector.detect(img)

		response = None
		if len(res) > 0:
			# Create python list of the objects of the format [class_name, object_location]
			objs = {}
			for obj in res:
				objs.update({obj[4]: []})

			for obj in res:
				if self.division == 1:
					location = self.__get_object_location1(obj[0], obj[1], obj[2], obj[3])
				else:
					location = self.__get_object_location2(obj[0], obj[1], obj[2], obj[3])
		
				objs[obj[4]].append(location)

			# Generate response using list
			response = self.__generate_response(objs)

		else:
			response = "Sorry, no objects were detected."

		return response
	
if __name__=="__main__":
	system = SceneDescribeSystem()
	system.run()
