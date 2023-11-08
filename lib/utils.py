import torchvision.transforms as transforms
import pandas as pd
import os
import cv2 as cv
import numpy as np

from lib.config import CONF


def data_pre_processing(driving_log):
    # data_pre_processing
    # use all three cameras' photos as the input
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

    return combined_images, combined_steering_angles


def argument_data_pre_processing(argument_driving_log):
    # argument_data_pre_processing
    # use all three cameras' photos as the input
    data = pd.read_csv(argument_driving_log, header=None)

    images = data[0].tolist()
    steering_angles = data[1].tolist()

    print('Finish loading argument images')

    return images, steering_angles


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

    return images, steering_angles, flip_images_path, flip_steering_angles


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
    delta_steering_angle_per_px = CONF.data_augmentation_translate.delta_steering_angle_per_px  # steering angle adjust
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
        steering_angle_adjust = steering_angles[idx] + translation_x * delta_steering_angle_per_px
        adjust_steering_angles.append(steering_angle_adjust)

        # translate matrix
        translate_matrix = np.float32([[1, 0, translation_x], [0, 1, translation_y]])

        translated_image = cv.warpAffine(image, translate_matrix, (cols, rows))

        translate_images_path.append(image_path)
        cv.imwrite(image_path, translated_image)

    images = images + translate_images_path
    steering_angles = steering_angles + adjust_steering_angles

    return images, steering_angles, translate_images_path, adjust_steering_angles


def data_augmentation_brightness(images, steering_angles):
    brightness_images_path = []

    if not os.path.exists(CONF.PATH.DATA_IMAGE_AUGMENTATION):  # create argumentation directory
        os.makedirs(CONF.PATH.DATA_IMAGE_AUGMENTATION)

    for idx in range(len(images)):
        image_name = os.path.basename(images[idx])  # get image name
        image_name = 'brightness_' + image_name

        image = cv.imread(images[idx])
        brightness_factor = np.random.uniform(0.3, 1.6)
        brightness_image = cv.convertScaleAbs(image, alpha=brightness_factor, beta=0)

        image_path = os.path.join(CONF.PATH.DATA_IMAGE_AUGMENTATION, image_name)
        brightness_images_path.append(image_path)

        cv.imwrite(image_path, brightness_image)

    images = images + brightness_images_path
    steering_angles_temp = steering_angles
    steering_angles = steering_angles + steering_angles

    return images, steering_angles, brightness_images_path, steering_angles_temp


def data_augmentation_random_shadow(images, steering_angles):
    shadow_images_path = []

    cols, rows = (CONF.data.image_size_rows, CONF.data.image_size_cols)
    w_low, w_high = (CONF.data_augmentation_random_shadow.w_low, CONF.data_augmentation_random_shadow.w_high)

    if not os.path.exists(CONF.PATH.DATA_IMAGE_AUGMENTATION):  # create argumentation directory
        os.makedirs(CONF.PATH.DATA_IMAGE_AUGMENTATION)

    for idx in range(len(images)):
        top_y = np.random.random_sample() * rows
        bottom_y = np.random.random_sample() * rows

        bottom_y_right = bottom_y + np.random.random_sample() * (rows - bottom_y)
        top_y_right = top_y + np.random.random_sample() * (rows - top_y)

        if np.random.random_sample() <= 0.5:
            bottom_y_right = bottom_y - np.random.random_sample() * bottom_y
            top_y_right = top_y - np.random.random_sample() * top_y
        poly = np.asarray([[[top_y, 0], [bottom_y, cols], [bottom_y_right, cols], [top_y_right, 0]]], dtype=np.int32)

        mask_weight = np.random.uniform(w_low, w_high)
        origin_weight = 1 - mask_weight

        image_name = os.path.basename(images[idx])  # get image name
        image_name = 'shadow_' + image_name

        image = cv.imread(images[idx])

        image_path = os.path.join(CONF.PATH.DATA_IMAGE_AUGMENTATION, image_name)
        shadow_images_path.append(image_path)

        mask = np.copy(image).astype(np.int32)
        cv.fillPoly(mask, poly, (0, 0, 0))
        # masked_image = cv2.bitwise_and(img, mask)
        shadow_image = cv.addWeighted(image.astype(np.int32), origin_weight, mask, mask_weight, 0).astype(np.uint8)

        cv.imwrite(image_path, shadow_image)

    images = images + shadow_images_path
    steering_angles_temp = steering_angles
    steering_angles = steering_angles + steering_angles

    return images, steering_angles, shadow_images_path, steering_angles_temp


def data_augmentation_random_erasing(images, steering_angles):
    erasing_images_path = []

    if not os.path.exists(CONF.PATH.DATA_IMAGE_AUGMENTATION):  # create argumentation directory
        os.makedirs(CONF.PATH.DATA_IMAGE_AUGMENTATION)

    for idx in range(len(images)):
        image_name = os.path.basename(images[idx])  # get image name
        image_name = 'erasing_' + image_name

        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.RandomErasing(p=1, scale=(0, 0.4), ratio=(0.5, 2.5), value=0, inplace=False),
            transforms.ToPILImage()
        ])

        image = cv.imread(images[idx])
        erasing_image = transform(image)

        image_path = os.path.join(CONF.PATH.DATA_IMAGE_AUGMENTATION, image_name)
        erasing_images_path.append(image_path)

        erasing_image.save(image_path)

    images = images + erasing_images_path
    steering_angles_temp = steering_angles
    steering_angles = steering_angles + steering_angles

    return images, steering_angles, erasing_images_path, steering_angles_temp


def jpg_to_tensor(image):
    transf = transforms.ToTensor()
    image_tensor = transf(image)
    return image_tensor
