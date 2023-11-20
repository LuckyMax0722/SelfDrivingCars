import pytorch_lightning as pl

from torch.utils.data import DataLoader, random_split
from RealCar.lib.config import CONF
from RealCar.lib.dataset import RealCarDataset
from RealCar.lib.utils import jpg_to_tensor


class RealCarDataModule(pl.LightningDataModule):
    def __init__(self, data_log=CONF.PATH.DATA_LOG,
                 batch_size=CONF.datamodule.batch_size,
                 train_val_split=CONF.datamodule.train_val_split,
                 transform=jpg_to_tensor):
        super().__init__()
        self.driving_log = data_log
        self.dataset = RealCarDataset()
        self.batch_size = batch_size
        self.train_val_split = train_val_split
        self.transform = transform
        self.validation_split = CONF.datamodule.train_val_split

    def setup(self, stage=None):
        if stage == 'fit' or stage is None:
            dataset_size = len(self.dataset)
            val_size = int(self.validation_split * dataset_size)
            train_size = dataset_size - val_size
            self.train_dataset, self.val_dataset = random_split(self.dataset, [train_size, val_size])

        print(f"Training samples: {len(self.train_dataset)}  Validation samples: {len(self.val_dataset)}")

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=16, pin_memory=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False, num_workers=16, pin_memory=True)


data_module = RealCarDataModule(data_log=CONF.PATH.DATA_LOG,
                                  batch_size=CONF.datamodule.batch_size,
                                  train_val_split=CONF.datamodule.train_val_split,
                                  transform=jpg_to_tensor)