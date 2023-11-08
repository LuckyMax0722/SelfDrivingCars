import os
from easydict import EasyDict

CONF = EasyDict()

# Main Path
CONF.PATH = EasyDict()
CONF.PATH.BASE = '/home/jiachen/SelfDrivingCars'  # TODO: change this
CONF.PATH.DATA = os.path.join(CONF.PATH.BASE, 'data')
CONF.PATH.DATA_VAL = os.path.join(CONF.PATH.BASE, 'data_val')
CONF.PATH.OUTPUT_MODEL = os.path.join(CONF.PATH.BASE, 'output/model/')

# Simulator Data
CONF.PATH.SIMULATOR_STEERING_ANGLE = os.path.join(CONF.PATH.DATA, "driving_log.csv")
CONF.PATH.SIMULATOR_STEERING_ANGLE_VAL = os.path.join(CONF.PATH.DATA_VAL, "driving_log.csv")
CONF.PATH.SIMULATOR_STEERING_ANGLE_ARGUMENT = os.path.join(CONF.PATH.DATA, "driving_log_a.csv")

CONF.PATH.DATA_IMAGE = os.path.join(CONF.PATH.DATA, "IMG")
CONF.PATH.DATA_IMAGE_AUGMENTATION = os.path.join(CONF.PATH.DATA, "IMG_A")

# Dataset
CONF.data = EasyDict()
CONF.data.source = 'Simulator'  # 'Download', 'Simulator'  # TODO: change this
CONF.data.image_size_rows = 160
CONF.data.image_size_cols = 320

# Data augmentation translate
CONF.data_augmentation_translate = EasyDict()
CONF.data_augmentation_translate.low_x_range = -60
CONF.data_augmentation_translate.high_x_range = 61
CONF.data_augmentation_translate.low_y_range = -20
CONF.data_augmentation_translate.high_y_range = 21
CONF.data_augmentation_translate.delta_steering_angle_per_px = 0.3 / 100

# Data augmentation shadow
CONF.data_augmentation_random_shadow = EasyDict()
CONF.data_augmentation_random_shadow.w_low = 0.6
CONF.data_augmentation_random_shadow.w_high = 0.85

# Datamodule
CONF.datamodule = EasyDict()
CONF.datamodule.batch_size = 150
CONF.datamodule.train_val_split = 0.9

# Best Model
CONF.model = EasyDict()
CONF.model.best_model = '/data/tumdriving/SelfDrivingCars/output/model/model_Second_Track_Same.pth'  # TODO: change this
