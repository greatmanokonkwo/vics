"""
This is an implementation of the AlexNet convolutional neural network. 
It was 2 output neurons, the halt signal and the angular displacement in time
"""
import torch
import torch.nn as nn

class GuideNet(nn.Module):
	def __init__(self):
		super().__init__()
		self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
		self.act1 = nn.Tanh()
		self.pool1 = nn.MaxPool2d(2)
		self.conv2 = nn.Conv2d(16, 8, kernel_size=3, padding=1)
		self.act2 = nn.Tanh()
		self.pool2 = nn.MaxPool2d(2)
		self.conv3 = nn.Conv2d(8, 4, kernel_size=3, padding=1)
		self.act3 = nn.Tanh()
		self.pool3 = nn.MaxPool2d(2)
		self.fc1 = nn.Linear(4*32*32, 1024) 
		self.act4 = nn.Tanh()
		self.fc2 = nn.Linear(1024, 512)
		self.act5 = nn.Tanh()
		self.fc3 = nn.Linear(512,2) 
		
	def forward(self, x):
		out = self.pool1(self.act1(self.conv1(x)))
		out = self.pool2(self.act2(self.conv2(x)))
		out = self.pool3(self.act3(self.conv3(x)))
		out = out.view(-1, 8*32*32)
		out = self.act4(self.fc1(out))
		out = self.act5(self.fc2(out))
		out = self.fc3(out)
