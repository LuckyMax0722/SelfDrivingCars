import csv
import os
import shutil

# read csv file
input_file = '/data/driving_log.csv'
output_file = '/home/jiachen/SelfDrivingCars/data/driving_log_new.csv'
output_folder = '/home/jiachen/SelfDrivingCars/data/IMG_new/'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def copy_image(image_path):
    image_filename = os.path.basename(image_path)
    target_path = os.path.join(output_folder, image_filename)

    try:
        shutil.copy(image_path, target_path)
        print(f"复制 {image_path} 到 {target_path}")
    except Exception as e:
        print(f"复制 {image_path} 失败: {str(e)}")


with open(input_file, 'r', newline='') as input_csvfile, open(output_file, 'w', newline='') as output_csvfile:
    csv_reader = csv.reader(input_csvfile)
    csv_writer = csv.writer(output_csvfile)

    for row in csv_reader:
        if len(row) >= 3 and row[3] != ' 0':
            # write new log
            csv_writer.writerow(row)

            center_image_path = row[0]
            left_image_path = row[1].strip()
            right_image_path = row[2].strip()

            copy_image(center_image_path)
            copy_image(left_image_path)
            copy_image(right_image_path)
