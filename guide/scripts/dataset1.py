import os
from PIL import Image
import torch.tensor
from torch.utils.data import Dataset
from torchvision import transforms
import pandas as pd
import matplotlib.pyplot as plt

class MotionData(Dataset):

	def __init__(self, data_json):
		self.data = pd.read_json(data_json, lines=True)
		self.transform = transforms.ToTensor()
		
	def __len__(self):
		return len(self.data)

	def __getitem__(self, idx):
		if torch.is_tensor(idx):
			idx = idx.item()
	
		file_path = self.data.key.iloc[idx]
		img_ = self.transform(Image.open(file_path))
		label = self.data.label.iloc[idx]
			
		return img_, label

if __name__=="__main__":
	data = MotionData(data_json="/home/greatman/code/vics/guide/neuralnet/train.json")
	plt.imshow(data[0][0])
	plt.show()
	print(data[0])
