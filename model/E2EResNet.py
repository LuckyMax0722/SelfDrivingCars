import pytorch_lightning as pl
import torch
import torch.nn as nn
import torchvision.models as models


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

    def training_step(self, batch):
        image, label = batch
        logits = self.model(image)
        logits = logits.squeeze(-1)
        loss = nn.MSELoss()(logits.float(), label.float())
        self.log('train_loss', loss, on_step=True, prog_bar=True, logger=True)

        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)

        # scheduler = StepLR(optimizer, step_size=1, gamma=0.9)  # 每个epoch后，学习率乘0.9
        return [optimizer]
