import os
from PIL import Image
import torch.tensor
from torch.utils.data import Dataset
from torchvision import transforms
import pandas as pd
import matplotlib.pyplot as plt
import cv2

class MotionData(Dataset):

	def __init__(self, data_json, reso=256):
		self.reso = reso
		self.data = pd.read_json(data_json, lines=True)

		trans = [transforms.ColorJitter(brightness=1, contrast=0.5, saturation=1, hue=0.5),
						transforms.GaussianBlur(kernel_size=31, sigma=5)]
		
		self.data_augment = transforms.RandomChoice(trans)

		self.transform = transforms.Compose([
							transforms.ToTensor(),
							transforms.Normalize((0.4849, 0.4798, 0.4740), 
												 (0.1678, 0.17325, 0.1815))
						 ])

	def __len__(self):
		return len(self.data)

	def __getitem__(self, idx):
		if torch.is_tensor(idx):
			idx = idx.item()
	
		file_path = self.data.key.iloc[idx]
		img_ = self.transform(Image.open(file_path))
		label = self.data.label.iloc[idx]
	
		return img_, label
	
	def create_data_augmentations(self):
		n = self.__len__()
		
		for idx in range(n):
			file_path = self.data.key.iloc[idx]
			img = Image.open(file_path)
			img_ = self.data_augment(img)
			aug_path = file_path.split('.')[0] + "_aug.jpg"
			img_.save(aug_path)
			print(idx, end="\r")
			
def augment():
	train_data.create_data_augmentations()
	test_data.create_data_augmentations()

def norm_vals():
	n = len(train_data)
	ends = [0, int(n/2), n]
	p = 1 # set p=0 for first half of data and p=1 for second half

	data = []
	for i in range(1):
		for j in range(ends[p], ends[p+1]):
			print(j, end="\r")
			data.append(train_data[j][0])

		imgs = torch.stack(data, dim=3)
		means_per_channel = imgs.view(3, -1).mean(dim=1)
		std_per_channel = imgs.view(3, -1).std(dim=1)
		print(means_per_channel)
		print(std_per_channel)
		print()

train_data = MotionData(data_json="/home/greatman/code/vics/guide/neuralnet/train.json")
#test_data = MotionData(data_json="/home/greatman/code/vics/guide/neuralnet/test.json")

if __name__=="__main__":
	norm_vals()
