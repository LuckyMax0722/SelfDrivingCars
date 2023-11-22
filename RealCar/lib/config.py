import os
from easydict import EasyDict

CONF = EasyDict()

# Main Path
CONF.PATH = EasyDict()
CONF.PATH.BASE = '/home/jiachen/SelfDrivingCars/RealCar'  # TODO: change this

# DATA_ORIGINAL
CONF.PATH.DATA_ORIGINAL = '/media/jiachen/LJC-2/data_original'
CONF.PATH.DATA_ORIGINAL_LOG = os.path.join(CONF.PATH.DATA_ORIGINAL, 'data.csv')
CONF.PATH.DATA_ORIGINAL_LOG_PROCESSED = os.path.join(CONF.PATH.DATA_ORIGINAL, 'data_processed.csv')


#DATA
CONF.PATH.DATA = os.path.join(CONF.PATH.BASE, 'data')
CONF.PATH.DATA_CENTER_IMAGES = os.path.join(CONF.PATH.DATA, 'center_rgb')
CONF.PATH.DATA_LEFT_IMAGES = os.path.join(CONF.PATH.DATA, 'left_rgb')
CONF.PATH.DATA_RIGHT_IMAGES = os.path.join(CONF.PATH.DATA, 'right_rgb')
CONF.PATH.DATA_LOG = os.path.join(CONF.PATH.DATA, 'data.csv')
CONF.PATH.DATA_IMAGE_AUGMENTATION = os.path.join(CONF.PATH.DATA, "IMG_A")
CONF.PATH.DATA_ARGUMENTATION = os.path.join(CONF.PATH.DATA, "data_A.csv")

# Dataset
CONF.data = EasyDict()
CONF.data.image_size_rows = 720
CONF.data.image_size_cols = 1280

# Data augmentation
CONF.data_augmentation = EasyDict()  # TODO: change the following
CONF.data_augmentation.flip = True
CONF.data_augmentation.translate = True
CONF.data_augmentation.brightness = True
CONF.data_augmentation.random_shadow = True
CONF.data_augmentation.random_erasing = True

# Data augmentation translate
CONF.data_augmentation_translate = EasyDict()
CONF.data_augmentation_translate.low_x_range = -140
CONF.data_augmentation_translate.high_x_range = 140
CONF.data_augmentation_translate.low_y_range = -80
CONF.data_augmentation_translate.high_y_range = 80
CONF.data_augmentation_translate.delta_steering_angle_per_px = 0.1 / 100

# Data augmentation shadow
CONF.data_augmentation_random_shadow = EasyDict()
CONF.data_augmentation_random_shadow.w_low = 0.6
CONF.data_augmentation_random_shadow.w_high = 0.85

# Datamodule
CONF.datamodule = EasyDict()
CONF.datamodule.batch_size = 8
CONF.datamodule.train_val_split = 0.1

