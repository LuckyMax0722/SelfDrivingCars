import sys
sys.path.append("./")

import socketio
import eventlet.wsgi
import base64
import torch

from io import BytesIO
from PIL import Image
from flask import Flask
from lib.config import CONF
from lib.utils import jpg_to_tensor
from model.E2EResNet import E2EResNet

sio = socketio.Server()
application = Flask(__name__)


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
            steering_angle = float(model(image_tensor))  # predict the steering angel based on input image

            global speed_limit
            if speed > speed_limit:
                speed_limit = MIN_SPEED
            else:
                speed_limit = MAX_SPEED

            throttle = 1.0 - steering_angle ** 2 - (speed/speed_limit) ** 2

            '''
            if abs(steering_angle) > 0.06:
                throttle = 0.2
                speed = 15
            else:
                throttle = 0.25
                speed = 20
            '''

            print('{} {} {}'.format(steering_angle, throttle, speed))
            send_control(steering_angle, throttle, speed)

        except Exception as e:
            print(e)
    else:
        sio.emit('manual', data={}, skip_sid=True)


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0.0, 0, 5)  # init


def send_control(steering_angle, throttle, speed):
    sio.emit("steer", data={
        'steering_angle': steering_angle.__str__(),
        'throttle': throttle.__str__(),
        'speed': speed.__str__()
    }, skip_sid=True)


if __name__ == '__main__':
    # define speed
    MAX_SPEED = 18
    MIN_SPEED = 10

    speed_limit = MAX_SPEED

    # load model
    model = E2EResNet()
    model.load_state_dict(torch.load(CONF.model.best_model))
    model.eval()

    # connect to simulator
    application = socketio.Middleware(sio, application)
    eventlet.wsgi.server(eventlet.listen(('', 4567)), application)
