import cv2 as cv

from torch.utils.data import Dataset
from lib.config import CONF
from lib.utils import jpg_to_tensor, data_pre_processing, argument_data_pre_processing

class SimulatorDataset(Dataset):
    def __init__(self, argument_driving_log=CONF.PATH.SIMULATOR_STEERING_ANGLE_ARGUMENT, transform=jpg_to_tensor):
        self.images, self.steering_angles = argument_data_pre_processing(argument_driving_log)
        self.transform = transform

    def __len__(self):
        if len(self.images) == len(self.steering_angles):
            return len(self.images)
        else:
            print("Dataset error")

    def __getitem__(self, item):
        image_path = self.images[item]
        image = cv.imread(image_path)
        steering_angle = self.steering_angles[item]

        if self.transform:
            image = self.transform(image)  # jpg to tensor

        return image, steering_angle


class SimulatorDataset_Val(Dataset):
    def __init__(self, driving_log=CONF.PATH.SIMULATOR_STEERING_ANGLE_VAL, transform=jpg_to_tensor):
        self.images, self.steering_angles = data_pre_processing(driving_log)

        self.transform = transform

    def __len__(self):
        if len(self.images) == len(self.steering_angles):
            return len(self.images)
        else:
            print("Dataset error")

    def __getitem__(self, item):
        image_path = self.images[item]
        image = cv.imread(image_path)
        steering_angle = self.steering_angles[item]

        if self.transform:
            image = self.transform(image)  # jpg to tensor

        return image, steering_angle
    

def image_show(input):
    image, label = input
    print(label)
    print(" ")
    print(image.size())
    print(" ")
    print(image)

# mydataset = SimulatorDataset()
# image_show(mydataset[0])
