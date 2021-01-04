import os
from PIL import Image
import torch.tensor
from torch.utils.data import Dataset

class MotionDataset(Dataset):
	def __init__(self, data_path, transform=None):
		self.DATA_PATH = data_path
		self.samples = [] 
		for i in range(10):
			# Create list of filenames for images class directory and create tuples of format (PILImage, Direction_class)
			images = os.listdir(self.DATA_PATH + "/" + str(i))

			# The filenames in data directory are structured as class/id_angle.jpg
			if transform is None:
				self.samples.extend([(Image.open(self.DATA_PATH + "/"+str(i)+"/" + filename), i) for filename in images])
			else:
				self.samples.extend([(transform(Image.open(self.DATA_PATH + "/"+str(i)+"/" + filename)), i) for filename in images])


	# Get length of data samples in images directory from stored length in file "last.txt"
	def __len__(self):
		return len(self.samples)
	
	def __getitem__(self, idx):
		if type(idx) != torch.Tensor:
			idx = torch.tensor(idx).view(-1)

		ret = []
		for i in idx:
			ret.append(self.samples[i])
		return ret
