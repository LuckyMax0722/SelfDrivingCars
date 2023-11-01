import sys
sys.path.append("./")


from lib.dataset import SimulatorDataset
from lib.config import CONF
from lib.utils import jpg_to_tensor
from torch.utils.data import DataLoader, random_split
from model.E2EResNet_Pytorch import E2EResNet

import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models


import datetime

os.environ['CUDA_LAUNCH_BLOCKING'] = "1"

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

test = train_dataset[0][0].to(device)
# define model
model = models.resnet50().to(device)

my_tensor = torch.zeros(32, 3, 160, 320)

output = model(my_tensor.to(device))
