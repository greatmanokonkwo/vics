"""download and/or process data"""
import os.sys
sys.path.append("../..")

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
			waveform, sr = torchaudio.load(file_path, normalization=False)
			if sr > self.sr:
				waveform = torchaudio.transforms.Resample(sr, self.sr)(waveform)
			mfcc = self.audio_transform(waveform)
			label = self.data.label.iloc[idx]

		except Exception as e:
			print(str(e), file_path)
			return self.__getitem__(torch.randint(0, len(self), (1,)))

		return mfcc, label
