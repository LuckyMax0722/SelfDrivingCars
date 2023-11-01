import sys
sys.path.append("./")

import pytorch_lightning as pl
from lib.dataset import SimulatorDataset, image_show
from lib.datamodule import SimulatorDataModule
from model.E2EResNet import E2EResNet
import torch

# prepare dataset and dataloader
data = SimulatorDataModule()

model = E2EResNet()

# Load pretrained model
file = '/home/jiachen/SelfDrivingCars/output/model/model_Resnet50.pth'
model.load_state_dict(torch.load(file), strict=True)

# start training
trainer = pl.Trainer(accelerator='gpu',
                     devices=1,
                     max_epochs=5,
                     log_every_n_steps=10,
                     )

trainer.fit(model, data)

# tensorboard --logdir=/home/jiachen/SelfDrivingCars/scripts/lightning_logs
# watch -n 0.5 -d nvidia-smi