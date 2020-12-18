import os
import datetime
import torch
from torch import optim
from torch.utils.data import DataLoader
from torchvision import transforms
from motion_dataset import MotionDataset
from GuideNet import GuideNet
	
device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))

"""
Multitask learning combined loss function with regression and classification loss functions
The weights for each loss is calculated using the GradNorm algorithm proposed in:
 
GradNorm: Gradient Normalization for Adaptive Loss Balancing in Deep Multitask Networks
	Zhao Chen, Vijay Badrinarayanan, Chen-Yu Lee, Andrew Rabinovich

"""
def multi_loss(target_1, pred_1, target_2, pred_2):

# training loop 
def training_loop(n_epochs, optimizer, model, loss_fn, train_loader, val_loader):
	len_train = len(train_loader)	
	len_val = len(val_loader)

	for epoch in range(1, n_epochs + 1):	
		loss_train = 0.0
		loss_val = 0.0

		# Calculate loss for the training set and backpropagate
		for imgs, angles, halts in train_loader:
			imgs = imgs.to(device=device)
			angles = angles.to(device=device)
			halts = halts.to(device=device)
				
			outputs = model(imgs)
			loss = loss_fn(angles, outputs[:,0], halts, outputs[:,1])	

			optimizer.zero_grad()
			loss.backward()
			optimzer.step()

			loss_train += loss.item()	

		# Calculate validation losses for each epoch
		with torch.no_grad():
			loss_val = 0.0
			for imgs, angles, halts in val_loader:
				imgs = ims.to(device=device)
				angles = angles.to(device=device)
				halts = halts.to(device=device)

				preds = model(imgs)
				loss = loss_fn(angles, preds[:,0], halts, preds[:,1])
			
				loss_val += loss.item()

		if epoch == 1 or epoch % 10 == 0:
			print("{} Epoch {}, Training loss {}, Validation loss {}".format(
				datetime.datetime.now(), epoch, loss_train / len_train, loss_val / len_val))

if __name__ == "__main__":
	bs = int(input("Batch size: "))	
	n_epochs = int(input("Number of epochs: "))

	# create dataset from the dataset/images directory with a format (img, angle, halt_signal)
	data_path = os.path.dirname(os.getcwd()) + "/dataset/"
	dataset = MotionDataset(data_path, transform=transforms.ToTensor())

	# Dataloader to feed the training loop 
	loader = DataLoader(dataset, batch_size=bs, shuffle=True)

	# Split train and val sets

	# Load model	
	model = GuideNet().to(device=device)
	model_path = os.getcwd() + "/guide_net.pt"

	if os.path.exists(model_path):
		model.load_state_dict(torch.load(model_path))
	
	# Train model 
	optimizer = optim.SGD(model.parameters(), lr=1e-2)

	training_loop(
		n_epochs = 100,
		optimizer = optimizer,
		model = model,
		loss_fn = multi_loss,
		train_loader = train_loader
	)

	# Save trained model
	torch.save(model.state_dict(), model_path)
