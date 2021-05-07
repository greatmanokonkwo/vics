import time
import numpy as np
import pytesseract
import cv2
import time

from imutils.object_detection import non_max_suppression
from playsound import playsound

class ReadingSystem:
	def __init__(self, width=928, height=928, min_confidence=0.5, padding=0.05):
		self.width = width
		self.height = height
		self.min_confidence = min_confidence
		self.padding = padding

		# load the pre-trained EAST text detector
		print("[INFO] Loading EAST text detector...")
		self.net = cv2.dnn.readNet("/home/greatman/code/vics/read/frozen_east_text_detection.pb")
		self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
		self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

	def __decode_predictions(self, scores, geometry):
		# grab the nubmer of rows and columsn from the scores volume, then
		# initialize our set of bounding box rectangles and corresponding
		# confidnece scores
		numRows, numCols = scores.shape[2:4]
		rects = []
		confidences = []
	
		# loop over the number of rows
		for y in range(0, numRows):
			# extract the scroes (probabilities), followed by the
			# geometrical data used to derive potential bounding box
			# coordinates that surround text
			scoresData = scores[0, 0, y]
			xData0 = geometry[0, 0, y]
			xData1 = geometry[0, 1, y]
			xData2 = geometry[0, 2, y]
			xData3 = geometry[0, 3, y]
			anglesData = geometry[0, 4, y]
	
			# loop over the number of columns
			for x in range(0, numCols):
				# if our score does not have sufficient probability,
				# ignore it
				if scoresData[x] < self.min_confidence:
					continue

				# compute the offset factor as our resulting feature
				# maps will be 4x smaller than the input image
				offsetX, offsetY = (x * 4.0, y * 4.0)

				# extract the rotation angle for the prediction and
				# then compute the sin and cosine
				angle = anglesData[x]
				cos = np.cos(angle)
				sin = np.sin(angle)

				# use the geometry volume to derive the width and height
				# of the bounding box
				h = xData0[x] + xData2[x]
				w = xData1[x] + xData3[x]

				# compute both the starting and ending (x, y)-coordinates
				# for the text prediction bounding box
				endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
				endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
				startX = int(endX - w)
				startY = int(endY - h)

				# add the bounding box coordinates and probability score
				# to our respective lists
				rects.append((startX, startY, endX, endY))
				confidences.append(scoresData[x])

		# return a tuple of the bounding boxes and associated confidences
		return rects, confidences

	def run(self):		
		start = time.time()
		# capture the input image that contains text to be read
		img = self.cam.capture_image()
		#img = cv2.imread("/home/greatman/code/vics/read/test.jpg")	

		start_t = time.time()
		orig = img.copy()
		origH, origW = img.shape[:2]
		
		# set the new width and height and then dtermine the ratio in change
		# for both the wicth and height
		newW, newH = (self.width, self.height)
		rW = origW / float(newW)
		rH = origH / float(newH)
		
		# resize the image and grab the new image dimensions	
		img = cv2.resize(img, (newW, newH))
		H, W = img.shape[:2]

		# EAST Text detector
		# define the two output layer names for the EAST detector model that
		# we are interested in -- the first is the output probabilities and the
		# second can be used to derive the bounding box coordinates of text
		layerNames = [
			"feature_fusion/Conv_7/Sigmoid",
			"feature_fusion/concat_3"]

		# load the pre-trained EAST text detector
		print("[INFO] Loading EAST text detector...")
		net = cv2.dnn.readNet("frozen_east_text_detection.pb")
		net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
		net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

		# construct a blob from the image and then perform a forward pass of 
		# the model to obtain the two output layer sets
		blob = cv2.dnn.blobFromImage(img, 1.0, (W, H),
			(123.68, 116.78, 103.94), swapRB=True, crop=False)
		self.net.setInput(blob)
		scores, geometry = self.net.forward(layerNames)

		# decode the predictions, then  apply non-maxima suppression to
		# suppress weak, overlapping bounding boxes
		rects, confidences = self.__decode_predictions(scores, geometry)
		boxes = non_max_suppression(np.array(rects), probs=confidences)

		start_t = time.time()

		# initialize the list of results
		results = []

		# loop over the bounding boxes
		count = 0
		for (startX, startY, endX, endY) in boxes:
			count += 1
			# scale the bounding box coordinates based on the respective
			# ratios
			startX = int(startX * rW)
			startY = int(startY * rH)
			endX = int(endX * rW)
			endY = int(endY * rH)

			# in order to obtain a better OCR of the text we can potentially
			# apply a bit of padding surrounding the bounding box -- here we
			# are computing the deltas in both the x and y directions
			dX = int((endX - startX) * self.padding)
			dY = int((endY - startY) * self.padding)

			# apply padding to each side of the bounding box, respectively
			startX = max(0, startX - dX)
			startY = max(0, startY - dY)
			endX = min(origW, endX + (dX * 2))
			endY = min(origH, endY + (dY * 2))

			# extract the actual padded ROI
			roi = orig[startY:endY, startX:endX]
			cv2.imwrite(f"img{count}.jpg", roi)	

			# in order to apply Tesseract v4 to OCR text we must supply
			# (1) a language, (2) an OEM flag of 4, indicating that the we
			# wish to use the LSTM neural net model for OCR, and finally
			# (3) an OEM value, in this case, 7 which implies that we are
			# treating the ROI as a single line of text
			config = ("-l eng --oem 1 --psm 7")
			text = pytesseract.image_to_string(roi, config=config)

			# add the bounding box coordinates and OCR'd text to the list
			# of results
			results.append(((startX, startY, endX, endY), text))
	
		results = sorted(results, key=lambda r:(r[0][1], r[0][0]))

		
		# loop over the results
		count =1 
		for ((startX, startY, endX, endY), text) in results:
			# display the text OCR'd by Tesseract
			print("OCR TEXT")
			print("========")
			print("{}\n".format(text))
			# strip out non-ASCII text so we can draw the text on the image
			# using OpenCV, then draw the text and a bounding box surrounding
			# the text region of the input image
			text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
			output = orig.copy()
			cv2.rectangle(output, (startX, startY), (endX, endY),
				(0, 0, 255), 2)
			cv2.putText(output, text, (startX, startY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
			cv2.imwrite(f"detect{count}.jpg", output)
			count+=1

		results = self.__sort_by_line(results)

		results = sorted(results, key=lambda r:(r[0][1], r[0][0]))
		response = ""
		for ((startX, startY, endX, endY), text) in results:
			text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
			text += " "
			response += text

		return response

	# we want to read the words on the image line by line and left to right
	# so we are given y-coordinates by the localization coordinates so we must group each of 
	# the words into lines by looking at their y-coordinates
	# since the results are sorted by their y-coordinates then we can see that 
	# if we get a large difference in y-coordinates between 2 words next to each other
	# then we know the second word must be the start of a newline
	# A large difference can be defined as being greater than the height of half the previous
	def __sort_by_line(self, results):
		results_by_line = [] # list of word results but each classified from 1 to n lines
		line = [results[0]] # list that stores the words of a line before they have been classifed. When a new line is found we clear this list
		
		count = 0 # line count

		n = len(results)

		for i in range(1, n):
			diff = abs(results[i-1][0][1] - results[i][0][1]) # calculate height difference between two words
			prev_height = results[i-1][0][3] - results[i-1][0][1] # calculate height of previous word
					
			if diff > (prev_height/2):  
				#print("newline") # DEBUG
				for word in line:
					new_word = ((word[0][0], count, word[0][2], word[0][3]), word[1]) # set the starty component of the word to its line class so we can sort by line number
					results_by_line.append(new_word)

				count+=1
				line = []
		
			line.append(results[i])
			#print(diff) # DEBUG

		for word in line: # add the words of the last line to the results list
			new_word = ((word[0][0], count, word[0][2], word[0][3]), word[1])
			results_by_line.append(new_word)

		return results_by_line	

if __name__=="__main__":
	system = ReadingSystem()
	system.run()
