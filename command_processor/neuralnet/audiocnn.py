import torch.nn as nn
import torch.nn.functional as F

class AudioCNN(nn.Module):

	def __init__(self, input_shape, batch_size=16, num_cats=3):
		super().__init__()
		self.conv1 = nn.Conv2d(1, 32, kernel_size = 3, stride=1, padding=1)
		self.bn1 = nn.BatchNorm2d(32)
		self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
		self.bn2 = nn.BatchNorm2d(64)
		self.dropout1 = nn.Dropout(0.25)
		self.dense1 = nn.Linear(64*(((input_shape[1]//2)//2)//2)*(((input_shape[2]//2)//2)//2),128)
		self.dropout2 = nn.Dropout(0.5)
		self.dense2 = nn.Linear(500, num_cats)

	def forward(self, x):
		x = self.conv1(x)
		x = F.relu(self.bn1(x))
		x = self.conv2(x)
		x = F.relu(self.bn2(x))
		x = F.max_pool2d(x, kernel_size=2) 
		x = self.dropout1(x)
		x = x.view(x.size(0),-1)
		x = F.relu(self.dense1(x))
		x = self.dropout2(x)
		x = self.dense2(x)

		return x
