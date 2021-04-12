"""
This is an implementation of the AlexNet convolutional neural network: 

ImageNet Classification with Deep Convolutional Neural Networks
	Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton
University of Toronto

that is revised to work for the GuideNet tasks of movement angle prediction and halt signalling
It outputs a softmax classification over 10 classes, 9 of which are angles of direction while the last one is the halt signal

Class 0 = -PI/2 rad
Class 1 = -3PI/8 rad
Class 2 = -PI/4 rad
Class 3 = -PI/8 rad
Class 4 = 0 rad
Class 5 = PI/8 rad
Class 6 = PI/4 rad
Class 7 = 3PI/8 rad
Class 8 = PI/2 rad
Class 9 = Halt Signal
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

class GuideCNN(nn.Module):
	def __init__(self, dropout_ratio=0.25):
		super().__init__()
		self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
		self.conv2 = nn.Conv2d(16, 8, kernel_size=3, padding=1)
		self.conv3 = nn.Conv2d(8, 4, kernel_size=3, padding=1)
		self.fc1 = nn.Linear(4*32*32, 1024) 
		self.fc2 = nn.Linear(1024, 512)
		self.fc3 = nn.Linear(512,6) 

		# Define proportion or neurons to dropout
		self.dropout = nn.Dropout(dropout_ratio)
		
	def forward(self, x):
		out = F.max_pool2d(F.relu(self.conv1(x)), 2)
		out = F.max_pool2d(F.relu(self.conv2(out)), 2)
		out = F.max_pool2d(F.relu(self.conv3(out)), 2)
		out = out.view(-1, 4*32*32)
		out = self.dropout(out)
		out = torch.tanh(self.fc1(out))
		out = self.dropout(out)
		out = torch.tanh(self.fc2(out))
		out = self.dropout(out)
		out = self.fc3(out)
		
		return out
