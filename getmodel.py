import torch

torch.hub.set_dir('model/')

torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)