import os
from PIL import Image
from torch.utils.data import Dataset

class MotionDataset(Dataset):
	def __init__(self, data_path, transform=None):
		self.DATA_PATH = data_path

		# create list of filenames for images in images in directory and create tuples of format (filename, angle, halt signal)
		no_halt_images = os.listdir(self.DATA_PATH + "/0")
		halt_images = os.listdir(self.DATA_PATH + "/1")

		# the filenames in data directory are structured as halt_signal/id_angle.jpg
		if transform is None:
			self.samples = [(Image.open(self.DATA_PATH + "/0/" + filename), int(filename.split("_")[1][0:-4]), 0) 
							 for filename in no_halt_images]

			self.samples.extend([(Image.open(self.DATA_PATH + "/1/" + filename), int(filename.split("_")[1][0:-4]), 1) 
							 for filename in halt_images])

		else:
			self.samples = [(transform(Image.open(self.DATA_PATH + "/0/" + filename)), int(filename.split("_")[1][0:-4]), 0) 
							 for filename in no_halt_images]

			self.samples.extend([(transform(Image.open(self.DATA_PATH + "/1/" + filename)), int(filename.split("_")[1][0:-4]), 1) 
							 for filename in halt_images])


	# Get length of data samples in images directory from stored length in file "last.txt"
	def __len__(self):
		file_path = self.DATA_PATH + "/last.txt"

		with open(file_path, "r") as f:
			len_dir = int(f.read()[:-1])

		return len_dir
	
	def __getitem__(self, idx):
		return self.samples[idx]	
