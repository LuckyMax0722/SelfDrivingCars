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