"""
Processes the output of the YOLO objection detection algorithm to get a list of object that were found in the image as well as their locations.
The engine then uses a text-to-speech module to say what was in the captured scenery
"""

class SceneDescribeSystem:
	# Raspbery Pi Cam
	
	# Electret Microphone

	# Speech to text module

	# YOLO model 

	def __init__(self):

	# Takes information of a box and returns the box location (left, front, right)
	def __get_object_location(self, x, y, w, h):

	# Process the output of the YOLO algorithm to return a list of object names and their locations
	def __list_objects(self, YOLO_out):
	
	# Take in a list of objects detected in scene and return an appropriate text response that describes the scene
	def __generate_response(self, object_list):

	#
	def run(self):
		# Capture image
	
		# Run inference
	
		# Return object list

		# Generate response using list

		# Turn generated response to speech
	
		# Send generated audio file to speakers
