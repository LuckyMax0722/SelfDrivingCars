import pandas as pd
import cv2 as cv

from torch.utils.data import Dataset
from lib.config import CONF
from lib.utils import jpg_to_tensor


class SimulatorDataset(Dataset):
    def __init__(self, driving_log=CONF.PATH.SIMULATOR_STEERING_ANGLE, transform=jpg_to_tensor):
        self.data = pd.read_csv(driving_log)
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        pre_path = '/home/jiachen/SelfDrivingCars/data/'
        image_path = pre_path + self.data.iloc[item, 0]
        image = cv.imread(image_path)
        steering_angle = self.data.iloc[item, 3]

        if self.transform:
            image = self.transform(image)

        return image, steering_angle


def image_show(input):
    image, label = input
    print(label)
    print(" ")
    print(image.size())
    print(" ")
    print(image)


#mydataset = SimulatorDataset()
#image_show(mydataset[0])
