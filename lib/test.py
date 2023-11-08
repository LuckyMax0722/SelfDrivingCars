import sys
sys.path.append("./")


from lib.dataset import SimulatorDataset, SimulatorDataset_Val
from lib.config import CONF
from lib.utils import jpg_to_tensor
from torch.utils.data import DataLoader, random_split
from model.E2EResNet_Pytorch import E2EResNet

import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models


from lib.utils import jpg_to_tensor
import datetime


val_dataset = SimulatorDataset_Val(CONF.PATH.SIMULATOR_STEERING_ANGLE_VAL, transform=jpg_to_tensor)
num_val = len(val_dataset)
    
print(f" Validation samples: {num_val}")
