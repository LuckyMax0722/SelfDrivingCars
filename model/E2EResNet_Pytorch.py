import torch.nn as nn
import torchvision.models as models


class E2EResNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = models.resnet50(pretrained=False)
        #  change the last output FC layer
        self.model.fc = nn.Sequential(
            nn.Linear(2048, 512),
            nn.ReLU(),
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )


    def forward(self, x):
        return self.model(x)
