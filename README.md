# Masterpraktikum - Simulation-Based Autonomous Driving in Crowded City (IN2106, IN4348)
# Technical University Munich - WS 2023/24

## End to End Learning for Self Driving Cars
### Introduction
This program is part of the Masterpraktikum - Simulation-Based Autonomous Driving in Crowded City at the Technical University of Munich. In this work, I basically reproduce the work of [End to End Learning for Self-Driving Cars](https://arxiv.org/pdf/1604.07316.pdf).

### Result

As you can see from the GIF below, the Resnet50-based self-driving model has been able to keep the car on the track for some distance, however the car eventually veers off the track.

### Installation
1. Environment requirements

* Python 3.8
* Pytorch 1.11
* CUDA 11.3

The following installation guild suppose ``python=3.8`` ``pytorch=1.11`` and ``cuda=11.3``. You may change them according to your system.

Create a conda virtual environment and activate it.
```
conda create -n SDC python=3.8
conda activate SDC
```

2. Clone the repository.
```
git clone https://github.com/avavavsf/End-to-End-Learning-for-Self-Driving-Cars.git
```

3. Install the dependencies.
```
conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch
pip install pytorch-lightning==2.0.2
pip install -r requirements.txt
```

### Simulator Preparation
* Simulator can be found at:
  * [Windows 64 bit](https://d17h27t6h515a5.cloudfront.net/topher/2016/November/5831f3a4_simulator-windows-64/simulator-windows-64.zip)
  * [Linux](https://d17h27t6h515a5.cloudfront.net/topher/2016/November/5831f0f7_simulator-linux/simulator-linux.zip)

### Data Preparation
* You can either collect data manually using the training mode in the simulator
* Or you can download the existing training [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/584f6edd_data/data.zip)

After acquiring the training data, please move the data folder to the root directory. Your folder should look like this:
```
SelfDrivingCars
├──data
│   ├── IMG
│       ├── center...
│       ├── ...
│       ├── left...
│       ├── ...
│       ├── right...
│       ├── ...
│   ├── driving_log.csv
```

### Training
You can use the following code to train your own model based on the default configuration or you can download the pre-trained model [here](https://drive.google.com/file/d/1je9zkc7ruVa-F6uovzH5fq_cWajqncOs/view?usp=sharing). However, before you do that, you must set the project path in ``lib/config.py``.
```shell
cd scripts
python train.py
```
Of course, you can also change the relevant configuration for customized training.

### Testing
Before you test the model, make sure the project path has been reset (see Section [Training](https://github.com/LuckyMax0722/End_to_End_Learning_for_Self_Driving_Cars#training)).
```shell
cd scripts
python drive.py
```
Finally open the simulator and select autonomous mode