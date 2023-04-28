import cv2
import torch
import numpy
import sys
import os
import time

# Load Model
YoloModel = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
YoloModel.to('cuda')
Classes = YoloModel.names

# Get Camera Frames :)
Camera = cv2.VideoCapture(0)

while Camera.isOpened():
    Success, Frame = Camera.read()
    if Success:
        # Display the frame
        cv2.imshow('Webcam', Frame)

        FrameNumpy = [Frame]
        Results = YoloModel(FrameNumpy)
        Labels = Results.xyxyn[0][:, -1].cpu().numpy()
        Cordinates = Results.xyxyn[0][:, :-1].cpu().numpy()
        os.system("clear")
        for I in range(len(Labels)):
            print(Classes[Labels[I]])

    else:
        print("Failed to get frame!")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Camera.release()
cv2.destroyAllWindows()