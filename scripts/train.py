import sys
sys.path.append("./")

import pytorch_lightning as pl
from lib.config import CONF
from lib.dataset import SimulatorDataset, image_show
from lib.datamodule import SimulatorDataModule
from model.E2EResNet import E2EResNet
import torch

# prepare dataset and dataloader
data = SimulatorDataModule()

model = E2EResNet()

# Load pretrained model
file = CONF.model.best_model
model.load_state_dict(torch.load(file), strict=True)

# start training
trainer = pl.Trainer(accelerator='gpu',
                     devices=[3],
                     max_epochs=10,
                     log_every_n_steps=10,
                     )

trainer.fit(model, data)

# tensorboard --logdir=/data/tumdriving/SelfDrivingCars/lightning_logs
# watch -n 0.5 -d nvidia-smi