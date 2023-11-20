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

    center_images = data[7].tolist()
    left_images = data[6].tolist()
    right_images = data[5].tolist()

    combined_images = center_images + left_images + right_images

    steering_angles_center = data[4].tolist()
    steering_angles_left = data[4].tolist()
    steering_angles_right = data[4].tolist()
    steering_angles_left = [steering_angle_left - (15 * 100 / 33) for steering_angle_left in steering_angles_left]
    steering_angles_right = [steering_angle_right + (15 * 100 / 33) for steering_angle_right in steering_angles_right]
    combined_steering_angles = steering_angles_center + steering_angles_left + steering_angles_right
    combined_steering_angles = normalize_steering_angles(combined_steering_angles)

    return combined_images, combined_steering_angles


def normalize_steering_angles(steering_angles):
    steering_angles = [x / 100 for x in steering_angles]
    steering_angles = [1 if x > 1 else x for x in steering_angles]
    steering_angles = [-1 if x < -1 else x for x in steering_angles]
    return steering_angles


def jpg_to_tensor(image):
    transf = transforms.ToTensor()
    image_tensor = transf(image)
    return image_tensor
