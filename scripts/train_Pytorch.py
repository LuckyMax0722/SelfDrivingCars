import sys
sys.path.append("./")


from lib.dataset import SimulatorDataset
from lib.config import CONF
from lib.utils import jpg_to_tensor
from torch.utils.data import DataLoader, random_split
from model.E2EResNet_Pytorch import E2EResNet


import torch
import torch.nn as nn
import torch.optim as optim

import datetime


# define gpu
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


# prepare dataset and dataloader
dataset = SimulatorDataset(driving_log=CONF.PATH.SIMULATOR_STEERING_ANGLE, transform=jpg_to_tensor)
num_samples = len(dataset)
num_train = int(CONF.datamodule.train_val_split * num_samples)  # split training and validation data
num_val = num_samples - num_train
print(f"Training samples: {num_train}  Validation samples: {num_val}")
train_dataset, val_dataset = random_split(dataset, [num_train, num_val])

train_loader = DataLoader(train_dataset, batch_size=CONF.datamodule.batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=CONF.datamodule.batch_size, shuffle=True)


# define model
model = E2EResNet().to(device)

# define loss and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# resume training
checkpoint = torch.load(CONF.model.best_model)  # load model
model.load_state_dict(checkpoint)

# train model
num_epochs = 10

for epoch in range(num_epochs):
    running_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data

        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)

        outputs = outputs.squeeze(-1)
        loss = criterion(outputs.float(), labels.float())  # use L2 loss
        running_loss = running_loss + loss.item()

        if (i) % 100 == 0:
            print(f'Epoch {epoch + 1}, Step {i + 1}, Training Loss: {running_loss / 100}')
            
        loss.backward()
        optimizer.step()
        

    print(f'Epoch {epoch + 1}, Training Loss: {running_loss / len(train_loader)}')

    # 在每个epoch结束后进行验证
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for i, data in enumerate(val_loader, 0):
            inputs, labels = data

            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)

            outputs = outputs.squeeze(-1)
            loss = criterion(outputs.float(), labels.float())  # use L2 loss

            val_loss = val_loss + loss.item()

    print(f'Epoch {epoch + 1}, Validation Loss: {val_loss / len(val_loader)}')
    model.train()

    # save model
    filename = CONF.PATH.OUTPUT_MODEL
    filename += 'model_'
    current_time = datetime.datetime.now()
    time_string = current_time.strftime("%H:%M:%S")
    filename += time_string
    filename += f'_epoch{epoch+1}.pth'

    torch.save(model.state_dict(), 'filename')

print('Finished Training')

