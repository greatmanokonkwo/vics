"""Training script"""

import os
os.sys.path.append("../..")

import argparse
import torch
import torch.nn as nn
import torch.utils.data as data
import torch.optim as optim
from dataset import MotionData
from model import GuideCNN
from sklearn.metrics import classification_report
from tabulate import tabulate
import matplotlib.pyplot as plt


def save_checkpoint(checkpoint_path, model, optimizer, scheduler, notes=None):
    torch.save({
        "notes": notes,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "scheduler_state_dict": scheduler.state_dict()
    }, checkpoint_path)


def binary_accuracy(preds, y):
    #round predictions to the closest integer
    rounded_preds = preds
    acc = rounded_preds.eq(y.view_as(rounded_preds)).sum().item() / len(y)
    return acc

def plot_loss_curves(train_losses, test_losses):
    plt.plot(train_losses, "r-+", linewidth=2, label="train")
    plt.plot(test_losses, "b-", linewidth=3, label="val")
    plt.legend(loc="upper right", fontsize=14)
    plt.xlabel("Epoch", fontsize=14)
    plt.ylabel("Cross Entropy Loss", fontsize=14)
    plt.plot()
    plt.show()

def test(test_loader, model, loss_fn, test_losses, device, epoch):
    print("\n starting test for epoch %s"%epoch)
    losses = []
    accs = []
    preds = []
    labels = []
    with torch.no_grad():
        for idx, (img, label) in enumerate(test_loader):
            img, label = img.to(device), label.to(device)
            output = model(img)
            loss = loss_fn(output, label)
            losses.append(loss.item())
            _, pred = torch.max(torch.sigmoid(output), dim=1)
            acc = binary_accuracy(pred, label)
            preds += torch.flatten(pred).cpu()
            labels += torch.flatten(label).cpu()
            accs.append(acc)
            print("Iter: {}/{}, accuracy: {}".format(idx, len(test_loader), acc), end="\r")

    avg_test_loss = sum(losses)/len(losses)
    test_losses.append(avg_test_loss)
    average_acc = sum(accs)/len(accs) 
    print('Average test Accuracy:', average_acc, "\n")
    report = classification_report(labels, preds)
    print(report)
    return average_acc, report, test_losses


def train(train_loader, model, optimizer, loss_fn, train_losses, device, epoch):
    print("\n starting train for epoch %s"%epoch)
    losses = []
    preds = []
    labels = []
    for idx, (img, label) in enumerate(train_loader):
        img, label = img.to(device), label.to(device=device, dtype=torch.int64)
        optimizer.zero_grad()
        output = model(img)
        # pred = F.sigmoid(output)
        loss = loss_fn(output, label)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())

        # get predictions and labels for report
        _, pred = torch.max(torch.sigmoid(output), dim=1)
        preds += torch.flatten(pred).cpu()
        labels += torch.flatten(label).cpu()

        print("epoch: {}, Iter: {}/{}, loss: {}".format(epoch, idx, len(train_loader), loss.item()), end="\r")

    avg_train_loss = sum(losses)/len(losses)
    train_losses.append(avg_train_loss)
    acc = binary_accuracy(torch.Tensor(preds), torch.Tensor(labels))
    print('avg train loss:', avg_train_loss, "avg train acc", acc)
    report = classification_report(torch.Tensor(labels).numpy(), torch.Tensor(preds).numpy())
    print(report)
    return acc, report, train_losses


def main(args):
    use_cuda = not args.no_cuda and torch.cuda.is_available()
    torch.manual_seed(1)
    device = torch.device('cuda' if use_cuda else 'cpu')

    train_dataset = MotionData(data_json=args.train_data_json, reso=args.reso)
    test_dataset = MotionData(data_json=args.test_data_json, reso=args.reso)

    kwargs = {'num_workers': args.num_workers, 'pin_memory': True} if use_cuda else {}
    train_loader = data.DataLoader(dataset=train_dataset,
                                        batch_size=args.batch_size,
                                        shuffle=True,
                                        **kwargs)
    test_loader = data.DataLoader(dataset=test_dataset,
                                        batch_size=args.eval_batch_size,
                                        shuffle=True,
                                        **kwargs)

    model = GuideCNN(reso=args.reso).to(device=device)
    params_path = "guide.pt"
    checkpoint_path = os.path.join(args.save_checkpoint_path, args.model_name + ".pt")
	
    if os.path.exists(params_path):
        print("Loading model weights from last checkpoint")
        model.load_state_dict(torch.load(params_path)["model_state_dict"])

    model = model.to(device)
    optimizer = optim.SGD(model.parameters(), lr=args.lr)
    loss_fn = nn.CrossEntropyLoss()

    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=2)

    best_train_acc, best_train_report = 0, None
    best_test_acc, best_test_report = 0, None
    best_epoch = 0

    train_losses, test_losses = [], []

    for epoch in range(args.epochs):
        print("\nstarting training with learning rate", optimizer.param_groups[0]['lr'])
        train_acc, train_report, train_losses = train(train_loader, model, optimizer, loss_fn, train_losses, device, epoch)
        test_acc, test_report, test_losses = test(test_loader, model, loss_fn, test_losses, device, epoch)

        # record best train and test
        if train_acc > best_train_acc:
            best_train_acc = train_acc
        if test_acc > best_test_acc:
            best_test_acc = test_acc

        # saves checkpoint if metrics are better than last
        if test_acc >= best_test_acc:
            print("found best checkpoint. saving model as", checkpoint_path)
            save_checkpoint(
                checkpoint_path, model, optimizer, scheduler,
                notes="train_acc: {}, test_acc: {}, epoch: {}".format(best_train_acc, best_test_acc, epoch),
            )
            best_train_report = train_report
            best_test_report = test_report
            best_epoch = epoch

        table = [["Train ACC", train_acc], ["Test ACC", test_acc],
                ["Best Train ACC", best_train_acc], ["Best Test ACC", best_test_acc],
                ["Best Epoch", best_epoch]]
        # print("\ntrain acc:", train_acc, "test acc:", test_acc, "\n",
        #     "best train acc", best_train_acc, "best test acc", best_test_acc)
        print(tabulate(table))

        #scheduler.step(train_acc)
	
    plot_loss_curves(train_losses, test_losses)

    print("Done Training...")
    print("Best Model Saved to", checkpoint_path)
    print("Best Epoch", best_epoch)
    print("\nTrain Report \n")
    print(best_train_report)
    print("\nTest Report\n")
    print(best_test_report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wake Word Training Script")
    parser.add_argument('--epochs', type=int, default=100, help='epoch size')
    parser.add_argument('--batch_size', type=int, default=32, help='size of batch')
    parser.add_argument('--eval_batch_size', type=int, default=32, help='size of batch')
    parser.add_argument('--lr', type=float, default=1e-2, help='learning rate')
    parser.add_argument('--model_name', type=str, default="guide", required=False, help='name of model to save')
    parser.add_argument('--save_checkpoint_path', type=str, default='.', help='Path to save the best checkpoint')
    parser.add_argument('--train_data_json', type=str, default='train.json', required=False, help='path to train data json file')
    parser.add_argument('--test_data_json', type=str, default='test.json', required=False, help='path to test data json file')
    parser.add_argument('--no_cuda', action='store_true', default=False, help='disables CUDA training')
    parser.add_argument('--num_workers', type=int, default=1, help='number of data loading workers')
    parser.add_argument('--hidden_size', type=int, default=128, help='lstm hidden size')
    parser.add_argument('--reso', type=int, default=256, help='Input image size')

    args = parser.parse_args()

    main(args)

