

# prepare dataset and dataloader
mydataset = SimulatorDataset()

image, label = mydataset[0]
image = image.unsqueeze(0)

model = E2EResNet()

output = model(image)
print(output)
#print(model)