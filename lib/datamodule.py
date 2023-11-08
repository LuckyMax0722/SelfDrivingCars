import pytorch_lightning as pl

from torch.utils.data import DataLoader, random_split
from lib.config import CONF
from lib.dataset import SimulatorDataset, SimulatorDataset_Val
from lib.utils import jpg_to_tensor


class SimulatorDataModule(pl.LightningDataModule):
    def __init__(self, driving_log=CONF.PATH.SIMULATOR_STEERING_ANGLE,
                 driving_log_val=CONF.PATH.SIMULATOR_STEERING_ANGLE_VAL,
                 batch_size=CONF.datamodule.batch_size,
                 train_val_split=CONF.datamodule.train_val_split,
                 transform=jpg_to_tensor):
        
        super().__init__()
        self.driving_log = driving_log
        self.driving_log_val = driving_log_val

        self.batch_size = batch_size
        self.train_val_split = train_val_split
        self.transform = transform

    def setup(self, stage=None):
        self.train_dataset = SimulatorDataset(self.driving_log, transform=self.transform)
        num_train = len(self.train_dataset)
        
        self.val_dataset = SimulatorDataset_Val(self.driving_log_val, transform=self.transform)
        num_val = len(self.val_dataset)
    
        print(f"Training samples: {num_train}  Validation samples: {num_val}")

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=32, pin_memory=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False, num_workers=32, pin_memory=True)


data_module = SimulatorDataModule(driving_log=CONF.PATH.SIMULATOR_STEERING_ANGLE,
                                  driving_log_val=CONF.PATH.SIMULATOR_STEERING_ANGLE_VAL,
                                  batch_size=CONF.datamodule.batch_size,
                                  train_val_split=CONF.datamodule.train_val_split,
                                  transform=jpg_to_tensor)
