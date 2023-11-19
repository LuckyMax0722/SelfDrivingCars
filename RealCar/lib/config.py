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
