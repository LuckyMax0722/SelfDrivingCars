import os
from easydict import EasyDict

CONF = EasyDict()

# Main Path
CONF.PATH = EasyDict()
CONF.PATH.BASE = '/home/jiachen/SelfDrivingCars'  # TODO: change this
CONF.PATH.DATA = os.path.join(CONF.PATH.BASE, 'data')
CONF.PATH.OUTPUT_MODEL = os.path.join(CONF.PATH.BASE, 'output/model/')

# Simulator Data
CONF.PATH.SIMULATOR_STEERING_ANGLE = os.path.join(CONF.PATH.DATA, "driving_log.csv")

# Dataset
CONF.data = EasyDict()
CONF.data.source = 'Download'  # 'Download', 'Simulator'  # TODO: change this

# Datamodule
CONF.datamodule = EasyDict()
CONF.datamodule.batch_size = 16
CONF.datamodule.train_val_split = 0.9
