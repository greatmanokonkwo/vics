import argparse
import cv2
import os
import matplotlib.pyplot as plt
import time

parser = argparse.ArgumentParser(description="Classifying guidenet data by hand")
parser.add_argument("--video", dest="videofile", help="Video data to be inputted in", default="output2.avi", type=str)
parser.add_argument("--destination_path", dest="data_path", help="Where is the labelled data going to be stored", default="/home/greatman/data/guide/", type=str)
args = parser.parse_args()

videofile = args.videofile
data_path = args.data_path

class_names = [-90, -45, 0, 45, 90, "halt"]

print(videofile)
cap = cv2.VideoCapture(videofile)

assert cap.isOpened(), "Cannot capture source"

plt.ion()
plt.show()

idx = 1310
count = 0

for i in range(count):
	ret, frame = cap.read()

while (cap.isOpened()):
	count += 1
	ret, frame = cap.read()

	if ret:
		plt.imshow(frame)

		direct_class = int(input(f"Direction class, Image Number- {count}, Index - {idx}: "))
		if direct_class == 7:
			print("Skipped image")
		else:
			idx += 1	
			cv2.imwrite(os.path.join(data_path, f"{direct_class-1}/{idx}_{class_names[direct_class-1]}.jpg"), frame)
		plt.clf()
		
cap.realease()
cap.destroyAllWindows()	
