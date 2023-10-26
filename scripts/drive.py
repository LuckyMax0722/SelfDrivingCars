import socketio
import eventlet.wsgi
import base64
import torch
import time

from io import BytesIO
from PIL import Image
from flask import Flask

from lib.utils import jpg_to_tensor
from model.E2EResNet import E2EResNet

sio = socketio.Server()
application = Flask(__name__)

#Speed limits
max_speed = 30
min_speed = 10

speed_limit = max_speed

@sio.on('telemetry')
def telemetry(sid, data):

    if data:
        steering_angle = float(data["steering_angle"])
        throttle = float(data["throttle"])
        speed = float(data["speed"])
        image = Image.open(BytesIO(base64.b64decode(data["image"])))

        image_tensor = jpg_to_tensor(image)
        image_tensor = image_tensor.unsqueeze(0)

        try:
            steering_angle = float(model(image_tensor))

            throttle = 0.1
            speed = 20

            print('{} {} {}'.format(steering_angle, throttle, speed))
            send_control(steering_angle, throttle, speed)

        except Exception as e:
            print(e)
    else:
        sio.emit('manual', data={}, skip_sid=True)


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0.0, 0.0, 5)


def send_control(steering_angle, throttle, speed):
    sio.emit("steer", data={
        'steering_angle': steering_angle.__str__(),
        'throttle': throttle.__str__(),
        'speed': speed.__str__()
    }, skip_sid=True)


if __name__ == '__main__':
    model = E2EResNet()  # 替换为你的模型类
    model.load_state_dict(torch.load('/home/jiachen/SelfDrivingCars/output/model/model1026_18:37:39_epoch19.pth'))
    model.eval()

    application = socketio.Middleware(sio, application)
    eventlet.wsgi.server(eventlet.listen(('', 4567)), application)
