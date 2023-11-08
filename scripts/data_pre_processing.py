import sys
sys.path.append("./")

import csv
import os

from lib.utils import data_pre_processing, data_augmentation_flip, data_augmentation_translate, data_augmentation_brightness
from lib.config import CONF

# Read original images from three cameras
images, steering_angles = data_pre_processing(CONF.PATH.SIMULATOR_STEERING_ANGLE)

# Create dirs for argument images and steering angles
if not os.path.exists(CONF.PATH.DATA_IMAGE_AUGMENTATION):  # create argumentation directory
    os.makedirs(CONF.PATH.DATA_IMAGE_AUGMENTATION)

# 1 Flipping images
images, steering_angles, flip_images_path, flip_steering_angles = data_augmentation_flip(images, steering_angles)
combined_data = list(zip(flip_images_path, flip_steering_angles))

# Create new CSV file for writing argument images and steering angles
csv_file = CONF.PATH.SIMULATOR_STEERING_ANGLE_ARGUMENT
with open(csv_file, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    for row in combined_data:
        csv_writer.writerow(row)

print('Finish flipping images')

# 2 Translate images
images, steering_angles, translate_images_path, adjust_steering_angles = data_augmentation_translate(images, steering_angles)
combined_data = list(zip(translate_images_path, adjust_steering_angles))

# Continue write
csv_file = CONF.PATH.SIMULATOR_STEERING_ANGLE_ARGUMENT
with open(csv_file, mode='a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    for row in combined_data:
        csv_writer.writerow(row)

print('Finish translate images')

# 3 Brightness images
images, steering_angles, brightness_images_path, steering_angles_temp = data_augmentation_brightness(images, steering_angles)
combined_data = list(zip(brightness_images_path, steering_angles_temp))

# Continue write
csv_file = CONF.PATH.SIMULATOR_STEERING_ANGLE_ARGUMENT
with open(csv_file, mode='a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    for row in combined_data:
        csv_writer.writerow(row)

print('Finish brightness images')

