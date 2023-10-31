import pytorch_lightning as pl
import torch
import torch.nn as nn
import torchvision.models as models
import datetime

from lib.config import CONF


class E2EResNet(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = models.resnet50(pretrained=True)
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

    def training_step(self, batch):
        image, label = batch
        logits = self(image)
        logits = logits.squeeze(-1)
        loss = nn.MSELoss()(logits.float(), label.float())  # use L2 loss
        self.log('train_loss', loss, on_step=True, prog_bar=True, logger=True)

        return loss

    def on_train_epoch_end(self):  # save the model
        params = self.state_dict()
        # to cpu
        params_cpu = {k: v.cpu() for k, v in params.items()}
        # save model file
        self.filename = CONF.PATH.OUTPUT_MODEL
        self.filename += 'model_'
        current_time = datetime.datetime.now()
        time_string = current_time.strftime("%H:%M:%S")
        self.filename += time_string
        self.filename += f'_epoch{self.current_epoch}.pth'
        torch.save(params_cpu, self.filename)
        return None

    def validation_step(self, batch, batch_idx):
        image, label = batch
        logits = self(image)
        logits = logits.squeeze(-1)
        loss = nn.MSELoss()(logits.float(), label.float())
        self.log('val_loss', loss, on_step=True, prog_bar=True, logger=True)

        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)

        # scheduler = StepLR(optimizer, step_size=1, gamma=0.9)  # 每个epoch后，学习率乘0.9
        return [optimizer]
