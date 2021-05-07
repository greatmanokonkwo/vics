"""download and/or process data"""
import torch
import torch.nn as nn
import torchaudio
import pandas as pd
from devs_and_utils.audio_utils import MFCC, get_featurizer, SpecAugment

class WakeWordData(torch.utils.data.Dataset):
	"""Load and process wakeword data"""

	def __init__(self, data_json, sample_rate=8000, valid=False):
		self.sr = sample_rate
		self.data = pd.read_json(data_json, lines=True)
		if valid:
			self.audio_transform = get_featurizer(sample_rate)
		else:
			self.audio_transform = nn.Sequential(
				get_featurizer(sample_rate),
				SpecAugment(rate=0.5)
			)

	def __len__(self):
		return len(self.data)

	def __getitem__(self, idx):
		if torch.is_tensor(idx):
			idx = idx.item()

		try:    
			file_path = self.data.key.iloc[idx]
			waveform, sr = torchaudio.load(file_path)
			if sr > self.sr:
				waveform = torchaudio.transforms.Resample(sr, self.sr)(waveform)
			mfcc = self.audio_transform(waveform)
			label = self.data.label.iloc[idx]

		except Exception as e:
			print(str(e), file_path)
			return self.__getitem__(torch.randint(0, len(self), (1,)))

		return mfcc, label

def norm_vals():
	n = len(train_data)
	ends = [0, int(n/
	p = 0

	data = []
	for i in range(ends[p], ends[p+1]):
		print(j, end="\r")
		data.append(train_data[j][0]
		
	imgs = torch.stack(data, dim=3)
	means_per_channel = imgs.view(3, -1).mean(dim=1)
	std_per_channel = imgs.view(3, -1).std(dim=1)
	print(means_per_channel)
	print(std_per_channel)
	print()

