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
		json_data = pd.read_json(data_json, lines=True)

		trans = [transforms.ColorJitter(brightness=1, contrast=0.5, saturation=1, hue=0.5),
						transforms.GaussianBlur(kernel_size=31, sigma=5)]
		
		self.data_augment = transforms.RandomChoice(trans)

		transform = transforms.ToTensor()

		self.data = []
		n = len(json_data)

		for i in range(n):
			print(i)
			file_path = json_data.key.iloc[i]
			img_ = transform(Image.open(file_path))
			label = json_data.label.iloc[i]
	
			self.data.append((img_, label))
		
	def __len__(self):
		return len(self.data)

	def __getitem__(self, idx):
		if torch.is_tensor(idx):
			idx = idx.item()
	
		return self.data[idx]
	
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
	print(1)
	imgs = torch.stack([img_t for img_t, _ in train_data], dim=3)
	print(imgs.shape)
	means_per_channel = imgs.view(3, -1).mean(dim=1)
	std_per_channel = imgs.view(3, -1).STD(dim=1)
	print(means_per_channel)
	print(std_per_channel)

	print(train_imgs)

train_data = MotionData(data_json="/home/greatman/code/vics/guide/neuralnet/train.json")
#test_data = MotionData(data_json="/home/greatman/code/vics/guide/neuralnet/test.json")

if __name__=="__main__":
	print(train_data[0])
	norm_vals()	
