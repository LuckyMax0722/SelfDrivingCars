import cv2 as cv

from torch.utils.data import Dataset
from RealCar.lib.config import CONF
from RealCar.lib.utils import jpg_to_tensor, data_pre_processing, argument_data_pre_processing


class RealCarDataset(Dataset):
    def __init__(self, data_log=CONF.PATH.DATA_LOG, argument_data_log=CONF.PATH.DATA_ARGUMENTATION, transform=jpg_to_tensor):
        # self.images, self.steering_angles = data_pre_processing(data_log)
        self.images, self.steering_angles = argument_data_pre_processing(argument_data_log)
        self.transform = transform

    def __len__(self):
        if len(self.images) == len(self.steering_angles):
            return len(self.images)
        else:
            print("Dataset error")

    def __getitem__(self, item):
        image_path = self.images[item]
        image = cv.imread(image_path)
        image = cv.resize(image, (240, 160))
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


#mydataset = RealCarDataset()
#image_show(mydataset[0])
#print(len(mydataset))
