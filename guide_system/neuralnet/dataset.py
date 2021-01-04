import os
from PIL import Image
from torch.utils.data import Dataset

class MotionDataset(Dataset):
	def __init__(self, data_path, transform=None):
		self.DATA_PATH = data_path

		for i in range(10):
			# Create list of filenames for images class directory and create tuples of format (PILImage, Direction_class)
			images = os.listdir(self.DATA_PATH + "/" + str(i))

			# The filenames in data directory are structured as class/id_angle.jpg
			if transform is None:
				self.samples = [(Image.open(self.DATA_PATH + "/"+str(i)+"/" + filename), i) 
								for filename in images]

			else:
				self.samples = [(transform(Image.open(self.DATA_PATH + "/"+str(i)+"/" + filename)), i) 
							 	for filename in images]


	# Get length of data samples in images directory from stored length in file "last.txt"
	def __len__(self):
		file_path = self.DATA_PATH + "/last.txt"

		with open(file_path, "r") as f:
			len_dir = int(f.read()[:-1])

		return len_dir
	
	def __getitem__(self, idx):
		return self.samples[idx]	
