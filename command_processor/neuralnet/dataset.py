import torch
import torch.nn as nn
import torchaudio
from audioutils import MFCC, get_featurizer, SpecAugment 

class CommandsDataset(Dataset):

	def __init__(self, data_path, transform=None, sample_rate=8000, valid=False):
		self.DATA_PATH = data_path
		self.data = []
		self.transform = transform

		for i in range(3):
			filenames = os.listdir(self.DATA_PATH + "/" str(i))
			for f in filenames:
				data.append((f, i))
	
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
			file_path = self.data[idx][0]
			waveform, sr = torchaudio.load(file_path, normalization=False)
			if sr > self.sr:
				waveform = torchaudio.transforms.Resample(sr, self.sr)(waveform)
			mfcc = self.audio_transform(waveform)
			label = self.data[idx][1]

		except Exception as e:
			print(str(e), file_path)
			return self.__getitem__(torch.randint(0, len(self), (1,)))

		return mfcc, label
