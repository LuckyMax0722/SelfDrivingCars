import sys

sys.path.append("./")

import os
import csv
import pandas as pd
import shutil

from RealCar.lib.config import CONF
from PIL import Image


def test(data_log):
    data = pd.read_csv(data_log, header=None)
    right_images = data[5].tolist()
    img = Image.open(right_images[0])
    img.show()


def images_path_process(data_log):
    # read csv file
    input_file = data_log
    output_file = CONF.PATH.DATA_ORIGINAL_LOG_PROCESSED

    with open(input_file, 'r') as input_csv, open(output_file, 'w', newline='') as output_csv:
        csv_reader = csv.reader(input_csv)
        csv_writer = csv.writer(output_csv)

        next(csv_reader)  # jump the head

        for row in csv_reader:
            row[5] = row[5].replace('/home/apollo/data_result_of_2023_11_13', CONF.PATH.DATA_ORIGINAL)
            row[6] = row[6].replace('/home/apollo/data_result_of_2023_11_13', CONF.PATH.DATA_ORIGINAL)
            row[7] = row[7].replace('/home/apollo/data_result_of_2023_11_13', CONF.PATH.DATA_ORIGINAL)
            csv_writer.writerow(row)

        print("Finish images path processing")


def copy_images_function(images, target_folder):
    # create dir if not dir
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # copy image
    for image_path in images:
        image_filename = os.path.basename(image_path)
        target_path = os.path.join(target_folder, image_filename)
        shutil.copy(image_path, target_path)

def copy_images(data_log):
    data = pd.read_csv(data_log, header=None)
    center_images = data[7].tolist()
    left_images = data[6].tolist()
    right_images = data[5].tolist()

    target_center_images_folder = CONF.PATH.DATA_CENTER_IMAGES
    target_left_images_folder = CONF.PATH.DATA_LEFT_IMAGES
    target_right_images_folder = CONF.PATH.DATA_RIGHT_IMAGES

    copy_images_function(center_images, target_center_images_folder)
    copy_images_function(left_images, target_left_images_folder)
    copy_images_function(right_images, target_right_images_folder)

    print("Finish copy images")

def images_path_after_process():
    # read csv file
    input_file = CONF.PATH.DATA_ORIGINAL_LOG_PROCESSED
    output_file = CONF.PATH.DATA_LOG

    with open(input_file, 'r') as input_csv, open(output_file, 'w', newline='') as output_csv:
        csv_reader = csv.reader(input_csv)
        csv_writer = csv.writer(output_csv)

        for row in csv_reader:
            row[5] = row[5].replace(CONF.PATH.DATA_ORIGINAL, CONF.PATH.DATA)
            row[6] = row[6].replace(CONF.PATH.DATA_ORIGINAL, CONF.PATH.DATA)
            row[7] = row[7].replace(CONF.PATH.DATA_ORIGINAL, CONF.PATH.DATA)
            csv_writer.writerow(row)

        print("Finish images path after processing")

if __name__ == "__main__":
    # Step 1: change the image path in the data_log
    images_path_process(CONF.PATH.DATA_ORIGINAL_LOG)
    # Step 2: Copy the useful images to the working dir
    copy_images(CONF.PATH.DATA_ORIGINAL_LOG_PROCESSED)
    # Step 3: change the image path in the data_log
    images_path_after_process()
