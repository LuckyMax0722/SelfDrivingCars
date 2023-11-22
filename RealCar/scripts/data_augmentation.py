import sys

sys.path.append("./")

import csv
import os

from RealCar.lib.config import CONF
from RealCar.lib.utils import data_pre_processing, data_augmentation_flip, data_augmentation_translate, \
    data_augmentation_brightness, data_augmentation_random_shadow, data_augmentation_random_erasing


def write_csv_file(images_path, steering_angles):
    combined_data = list(zip(images_path, steering_angles))

    # Create new CSV file for writing argument images and steering angles
    csv_file = CONF.PATH.DATA_ARGUMENTATION
    with open(csv_file, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        for row in combined_data:
            csv_writer.writerow(row)


if __name__ == "__main__":
    # Create dirs for argument images and steering angles
    if not os.path.exists(CONF.PATH.DATA_IMAGE_AUGMENTATION):  # create argumentation directory
        os.makedirs(CONF.PATH.DATA_IMAGE_AUGMENTATION)

    # Define CSV file for writing argument information
    csv_file = CONF.PATH.DATA_ARGUMENTATION
    with open(csv_file, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

    # 0 Read original images from three cameras
    images, steering_angles = data_pre_processing(CONF.PATH.DATA_LOG)
    write_csv_file(images, steering_angles)
    print('Finish loading images')

    # 1 Flip images
    if CONF.data_augmentation.flip:
        images, steering_angles, flip_images_path, flip_steering_angles = data_augmentation_flip(images,
                                                                                                 steering_angles)
        write_csv_file(flip_images_path, flip_steering_angles)
        print('Finish flipping images')
    else:
        print('NO flipping images')

    # 2 Translate images
    if CONF.data_augmentation.translate:
        images, steering_angles, translate_images_path, adjust_steering_angles = data_augmentation_translate(images,
                                                                                                             steering_angles)
        write_csv_file(translate_images_path, adjust_steering_angles)
        print('Finish translate images')
    else:
        print('NO translate images')

    # 3 Brightness images
    if CONF.data_augmentation.brightness:
        images, steering_angles, brightness_images_path, steering_angles_temp = data_augmentation_brightness(images,
                                                                                                             steering_angles)
        write_csv_file(brightness_images_path, steering_angles_temp)
        print('Finish brightness images')
    else:
        print('NO brightness images')

    # 4 Random Shadow images
    if CONF.data_augmentation.random_shadow:
        images, steering_angles, shadow_images_path, steering_angles_temp = data_augmentation_random_shadow(images,
                                                                                                            steering_angles)
        write_csv_file(shadow_images_path, steering_angles_temp)
        print('Finish shadow images')
    else:
        print('NO shadow images')

    # 5 Random Erasing images
    if CONF.data_augmentation.random_erasing:
        images, steering_angles, erasing_images_path, steering_angles_temp = data_augmentation_random_erasing(
            images,
            steering_angles)
        write_csv_file(erasing_images_path, steering_angles_temp)
        print('Finish erasing images')
    else:
        print('NO erasing images')
