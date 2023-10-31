import torchvision.transforms as transforms
import pandas as pd
import os
import cv2 as cv
import numpy as np

from lib.config import CONF


def data_pre_processing(driving_log):
    # data_pre_processing
    # use all three cameras' photoes as the input
    if CONF.data.source == 'Download':
        data = pd.read_csv(driving_log)

        center_images = data['center'].tolist()
        left_images = data['left'].tolist()
        left_images = [s[1:] for s in left_images]
        right_images = data['right'].tolist()
        right_images = [s[1:] for s in right_images]
        combined_images = center_images + left_images + right_images
        combined_images = [os.path.join(CONF.PATH.DATA, image_path) for image_path in combined_images]

        steering_angles_center = data['steering'].tolist()
        steering_angles_left = data['steering'].tolist()
        steering_angles_right = data['steering'].tolist()
        steering_angles_left = [steering_angle_left + 0.25 for steering_angle_left in steering_angles_left]
        steering_angles_right = [steering_angle_right - 0.25 for steering_angle_right in steering_angles_right]
        combined_steering_angles = steering_angles_center + steering_angles_left + steering_angles_right

    elif CONF.data.source == 'Simulator':
        data = pd.read_csv(driving_log, header=None)

        center_images = data[0].tolist()
        left_images = data[1].tolist()
        left_images = [s[1:] for s in left_images]
        right_images = data[2].tolist()
        right_images = [s[1:] for s in right_images]
        combined_images = center_images + left_images + right_images

        steering_angles_center = data[3].tolist()
        steering_angles_left = data[3].tolist()
        steering_angles_right = data[3].tolist()
        steering_angles_left = [steering_angle_left + 0.25 for steering_angle_left in steering_angles_left]
        steering_angles_right = [steering_angle_right - 0.25 for steering_angle_right in steering_angles_right]
        combined_steering_angles = steering_angles_center + steering_angles_left + steering_angles_right

    else:
        print("Data source input error, please check the configuration file")

    return combined_images, combined_steering_angles


def data_augmentation_flip(images, steering_angles):
    flip_images_path = []

    if not os.path.exists(CONF.PATH.DATA_IMAGE_AUGMENTATION):  # create argumentation directory
        os.makedirs(CONF.PATH.DATA_IMAGE_AUGMENTATION)

    for idx in range(len(images)):
        image_name = os.path.basename(images[idx])  # get image name
        image_name = 'flip_' + image_name

        image = cv.imread(images[idx])
        flipped_image = cv.flip(image, 1)  # flip all images
        image_path = os.path.join(CONF.PATH.DATA_IMAGE_AUGMENTATION, image_name)
        flip_images_path.append(image_path)

        cv.imwrite(image_path, flipped_image)

    images = images + flip_images_path

    flip_steering_angles = [-x for x in steering_angles]  # inverse steering angles
    steering_angles = steering_angles + flip_steering_angles

    return images, steering_angles


def data_augmentation_translate(images, steering_angles):
    translate_images_path = []
    adjust_steering_angles = []

    if not os.path.exists(CONF.PATH.DATA_IMAGE_AUGMENTATION):  # create argumentation directory
        os.makedirs(CONF.PATH.DATA_IMAGE_AUGMENTATION)

    # translate parameters
    low_x_range = CONF.data_augmentation_translate.low_x_range
    high_x_range = CONF.data_augmentation_translate.high_x_range
    low_y_range = CONF.data_augmentation_translate.low_y_range
    high_y_range = CONF.data_augmentation_translate.high_y_range
    #delta_steering_angle_per_px = CONF.data_augmentation_translate.delta_steering_angle_per_px  # steering angle adjust
    rows, cols = (CONF.data.image_size_rows, CONF.data.image_size_cols)

    for idx in range(len(images)):
        image_name = os.path.basename(images[idx])  # get image name
        image_name = 'translate_' + image_name

        image = cv.imread(images[idx])

        image_path = os.path.join(CONF.PATH.DATA_IMAGE_AUGMENTATION, image_name)

        # random translate paras
        translation_x = np.random.randint(low_x_range, high_x_range)
        translation_y = np.random.randint(low_y_range, high_y_range)

        # adjust steering angle
        #steering_angle_adjust = steering_angles[idx] + translation_x * delta_steering_angle_per_px
        #adjust_steering_angles.append(steering_angle_adjust)

        # translate matrix
        translate_matrix = np.float32([[1, 0, translation_x], [0, 1, translation_y]])

        translated_image = cv.warpAffine(image, translate_matrix, (cols, rows))

        translate_images_path.append(image_path)
        cv.imwrite(image_path, translated_image)

    images = images + translate_images_path
    steering_angles = steering_angles + steering_angles

    return images, steering_angles


def jpg_to_tensor(image):
    transf = transforms.ToTensor()
    image_tensor = transf(image)
    return image_tensor
