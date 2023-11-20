import sys
sys.path.append("./")

import pytorch_lightning as pl
from RealCar.lib.config import CONF
from RealCar.lib.dataset import RealCarDataset
from RealCar.lib.datamodule import RealCarDataModule
from model.E2EResNet import E2EResNet
import torch

# prepare dataset and dataloader
data = RealCarDataModule()

model = E2EResNet()

# Load pretrained model
#file = CONF.model.best_model
#model.load_state_dict(torch.load(file), strict=True)

# start training
trainer = pl.Trainer(accelerator='gpu',
                     devices=1,
                     max_epochs=1,
                     log_every_n_steps=10,
                     limit_train_batches=1
                     )

trainer.fit(model, data)

# tensorboard --logdir=/data/tumdriving/SelfDrivingCars/lightning_logs
# watch -n 0.5 -d nvidia-smi