import pytorch_lightning as pl

from torch.utils.data import DataLoader, random_split
from lib.config import CONF
from lib.dataset import SimulatorDataset
from lib.utils import jpg_to_tensor


class SimulatorDataModule(pl.LightningDataModule):
    def __init__(self, driving_log=CONF.PATH.SIMULATOR_STEERING_ANGLE,
                 batch_size=CONF.datamodule.batch_size,
                 train_val_split=CONF.datamodule.train_val_split,
                 transform=jpg_to_tensor):
        super().__init__()
        self.driving_log = driving_log
        self.batch_size = batch_size
        self.train_val_split = train_val_split
        self.transform = transform

    def setup(self, stage=None):
        dataset = SimulatorDataset(self.driving_log, transform=self.transform)
        num_samples = len(dataset)
        num_train = int(self.train_val_split * num_samples)  # split training and validation data
        num_val = num_samples - num_train
        print(f"Training samples: {num_train}  Validation samples: {num_val}")
        self.train_dataset, self.val_dataset = random_split(dataset, [num_train, num_val])

    def train_dataloader(self):
        print("train data: ", len(self.train_dataset))
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size)


data_module = SimulatorDataModule(driving_log=CONF.PATH.SIMULATOR_STEERING_ANGLE,
                                  batch_size=CONF.datamodule.batch_size,
                                  train_val_split=CONF.datamodule.train_val_split,
                                  transform=jpg_to_tensor)
