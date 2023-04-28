import cv2
import torch
import numpy
import sys

# Load Model
YoloModel = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
YoloModel.to('cuda')

# Get Camera Frames :)
Camera = cv2.VideoCapture(0)

while Camera.isOpened():
    Success, Frame = Camera.read()

    cv2.imshow('Webcam', Frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Camera.release()
cv2.destroyAllWindows()