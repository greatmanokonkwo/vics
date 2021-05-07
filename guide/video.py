import os
import cv2
import torch
import time
import argparse
from neuralnet.GuideCNN import GuideCNN
from torchvision import transforms
import math

def arg_parse():
	"""
	Parse arguments to the detect module
	"""

	parser = argparse.ArgumentParser(description="Navigation Module Video Demo Detection")
	parser.add_argument("--fps", dest = "fps", help = "What fps was the video shot in", default=15, type=int)
	parser.add_argument("--width", dest = "width", help = "Width of video", default=192, type=int)
	parser.add_argument("--height", dest = "height", help = "Height of video", default=144, type=int)
	parser.add_argument("--video", dest = "videofile", help = "Video file to run detection demo on", default="video.avi", type=str)
	parser.add_argument("--output", dest = "out", help = "Video file to save demo on", default="output.avi", type=str)
	parser.add_argument("--reso", dest = "reso", help = "Model resolution", default=256, type=int)
	


	return parser.parse_args()

def write(img, direct_class):

	arrow_length = 50
	angle = 0	

	if direct_class != 5:
		angle = -1*classes[direct_class]
		label = f"{classes[direct_class]}"
	else:
		label = "STOP"

	y = abs(int(arrow_length * math.sin(math.radians(angle))))
	x = int(arrow_length * math.cos(math.radians(angle)))

	print(y, x)

	start_x, start_y = int(args.width/2), int(args.height - arrow_length)
	end_x, end_y = int(start_x + x), int(start_y - y)

	img = cv2.arrowedLine(img, (start_x, start_y), (end_x, end_y), (225, 225, 225), 6, tipLength = 0.5)
	img = cv2.putText(img, label, (int(args.width/2), 50), cv2.FONT_HERSHEY_PLAIN, 1, [225,255,255], 2, cv2.LINE_AA);	

	return img

args = arg_parse()

CUDA = torch.cuda.is_available()
device = "cuda" if CUDA else "cpu"
model = GuideCNN().to(device=device)
params_path = os.getcwd() + "/neuralnet/guide_net.pt"
if os.path.exists(params_path):
	model.load_state_dict(torch.load(params_path))

tensor = transforms.ToTensor()
softmax = torch.nn.Softmax(dim=0)

classes = [-90, -45, 0, 45, 90]	

videofile = args.videofile

cap = cv2.VideoCapture(videofile)

assert cap.isOpened(), "Cannot capture source"

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(args.out, fourcc, args.fps, (args.width, args.height))

start = time.time()

count = 0

while cap.isOpened():
	ret, frame = cap.read()

	if ret:
		if count == 0:
			img = tensor(cv2.resize(frame, (args.reso, args.reso), interpolation=cv2.INTER_CUBIC)).to(device=device)
			direct_class = torch.max(softmax(model(img.unsqueeze(0))[0]), dim=0)[1].item()		
	
		if count == args.fps:
			count = -1
		
		frame = write(frame, direct_class)
	
		out.write(frame)	
			
		cv2.imshow("frame", frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break	

		count+=1	

cap.release()
out.release()
cv2.destroyAllWindow()
