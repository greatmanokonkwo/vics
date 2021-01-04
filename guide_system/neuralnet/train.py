import os
import datetime
import torch
from torch import optim
from torch.utils.data import DataLoader
from torchvision import transforms
import torch.nn as nn
from dataset import MotionDataset
from GuideNet import GuideNet
	
device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))

"""
Multitask learning combined loss function with regression and classification loss functions
The weights for each loss is calculated using the GradNorm algorithm proposed in:
 
GradNorm: Gradient Normalization for Adaptive Loss Balancing in Deep Multitask Networks
	Zhao Chen, Vijay Badrinarayanan, Chen-Yu Lee, Andrew Rabinovich

"""
# training loop 
def training_loop(n_epochs, optimizer, model, loss_fn, train_loader, val_loader):
	len_train = len(train_loader)	
	len_val = len(val_loader)

	for epoch in range(1, n_epochs + 1):	
		loss_train = 0.0
		loss_val = 0.0

		# Calculate loss for the training set and backpropagate
		for imgs, classes in train_loader:
			imgs = imgs.to(device=device)
			classes = classes.to(device=device)
				
			outputs = model(imgs)
			loss = loss_fn(outputs, classes)	

			optimizer.zero_grad()
			loss.backward()
			optimzer.step()

			loss_train += loss.item()	

		# Calculate validation losses for each epoch
		with torch.no_grad():
			loss_val = 0.0
			for imgs, classes in val_loader:
				imgs = ims.to(device=device)
				classes = classes.to(device=device)

				preds = model(imgs)
				loss = loss_fn(outputs, classes)	
			
				loss_val += loss.item()

		if epoch == 1 or epoch % 10 == 0:
			print("{} Epoch {}, Training loss {}, Validation loss {}".format(
				datetime.datetime.now(), epoch, loss_train / len_train, loss_val / len_val))

if __name__ == "__main__":
	val_size = float(input("Validation set ratio (Ex: 0.2): "))
	bs = int(input("Batch size: "))	
	n_epochs = int(input("Number of epochs: "))

	# create dataset from the dataset/images directory with a format (img, angle, halt_signal)
	data_path = str(input("Please specify the location of the GuideNet dataset:"))
	dataset = MotionDataset(data_path, transform=transforms.ToTensor())

	# Split the dataset
	n_samples = len(dataset)
	n_val = int(0.2 * n_samples)
	shuffled_indices = torch.randperm(n_samples)
	
	train_indices = shuffled_indices[:-n_val]
	val_indices = shuffled_indices[-n_val:]
	
	# Dataloader to feed the training loop 
	train_loader = DataLoader(dataset[train_indices], batch_size=bs, shuffle=True)
	val_loader = DataLoader(dataset[val_indices], batch_size=bs, shuffle=True)

	for i, batch in enumerate(val_loader):
		print (batch)	

	# Split train and val sets

	# Load model	
	model = GuideNet().to(device=device)
	model_path = os.getcwd() + "/guide_net.pt"

	if os.path.exists(model_path):
		model.load_state_dict(torch.load(model_path))
	
	# Train model 
	optimizer = optim.SGD(model.parameters(), lr=1e-2)
	loss_fn = nn.CrossEntropyLoss()

	training_loop(
		n_epochs = n_epochs,
		optimizer = optimizer,
		model = model,
		loss_fn = loss_fn,
		train_loader = train_loader,
		val_loader = val_loader	
	)

	# Save trained model
	torch.save(model.state_dict(), model_path)
