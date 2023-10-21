import pytorch_lightning as pl
from lib.dataset import SimulatorDataset, image_show
from lib.datamodule import SimulatorDataModule
from model.E2EResNet import E2EResNet

# prepare dataset and dataloader
'''
mydataset = SimulatorDataset()
image, label = mydataset[0]
image = image.unsqueeze(0)
'''
data = SimulatorDataModule()

model = E2EResNet()

# start training
trainer = pl.Trainer(accelerator='gpu',
                     devices=1,
                     max_epochs=20,
                     log_every_n_steps=10,
                     )

trainer.fit(model, data)

# tensorboard --logdir=/home/jiachen/SelfDrivingCars/scripts/lightning_logs