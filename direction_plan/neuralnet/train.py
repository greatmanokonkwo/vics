<<<<<<< HEAD
import torch
from torchvision import transforms
import GuideNET

=======
import os
import datetime
import torch
from torch import optim
from torch.utils.data import DataLoader
from torchvision import transforms
from motion_dataset import MotionDataset
from GuideNet import GuideNet
	
device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))

# multitask learning combined loss function with regression and classification loss functions
def multi_loss(ground_truth, out1, out2):
	

# training loop 
def training_loop(n_epochs, optimizer, model, loss_fn, train_loader):
	len_train = len(train_loader)
	for epoch in range(1, n_epochs + 1):	
		loss_train1 = 0.0
		loss_train2 = 0.0

		for imgs, angles, halts in train_loader:
			imgs = imgs.to(device=device)
			angles = angles.to(device=device)
			halts = hals.to(device=device)
				
			outputs = model(imgs)
			loss = loss_fn(outputs, angle, halt)	
			
		if epoch == 1 or epoch % 10 == 0:
			print("{} Epoch {}, Training loss 1 {}, Training loss 2 {}".format(
				datetime.datetime.now(), epoch, loss_train1 / len_train, loss_train2 / len_train))

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
	
>>>>>>> 8f97b5e3445e9d04d8ebf9d77fd420118d62dda5
