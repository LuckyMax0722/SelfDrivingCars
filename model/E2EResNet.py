import pytorch_lightning as pl
import torch
import torch.nn as nn
import torchvision.models as models

from lib.dataset import SimulatorDataset, image_show

class E2EResNet(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = models.resnet50(pretrained=False)
        self.model.fc = nn.Sequential(
            nn.Linear(2048, 512),
            nn.ReLU(),
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        return self.model(x)

    def training_step(self, *args: Any, **kwargs: Any) -> STEP_OUTPUT: