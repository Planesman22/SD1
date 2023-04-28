import cv2
import torch
import numpy
import sys
import os
import time
import socket
import json

RecieverIP = "131.247.10.146"

# Load Model
YoloModel = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
YoloModel.to('cpu')
Classes = YoloModel.names

# Prep Socket
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.bind((RecieverIP, 96385))
ServerSocket.listen(1)
print("Server is waiting for a connection...")

ClientSocket, ClientAddress = ServerSocket.accept()
print("Connected to: ", str(ClientAddress)+"!")

# Get Camera Frames :)
Camera = cv2.VideoCapture(0)

_, LastFrame = Camera.read()

while Camera.isOpened():
    _, Frame = Camera.read()
    FrameWidth = Frame.shape[1]
    FrameHeight = Frame.shape[0]

    FrameNumpy = [Frame]
    Results = YoloModel(FrameNumpy).xyxyn[0].numpy()

    # Generate our feature  vector
    PVector = numpy.zeros((len(Classes), 4))
    for I in range(PVector.shape[0]):
        PVector[I, 0] = I

    # Class probabilities and Size
    for I in Results:
        Class = int(I[5])
        Probability = I[4]
        if Probability > PVector[Class, 1]:
            TargetX = I[0]
            TargetY = I[1]
            TargetW = I[2]
            TargetH = I[3]

            PVector[Class, 1] = Probability
            PVector[Class, 2] = TargetW * TargetH

            # Crops
            Y1 = int(TargetY * FrameHeight)
            Y2 = int(TargetH * FrameHeight)
            X1 = int(TargetX * FrameWidth)
            X2 = int(TargetW * FrameWidth)
            # cv2.imshow(Classes[Class], Frame[Y1:Y2,X1:X2])

            # Optical Flow, gray scale only
            GrayA = cv2.cvtColor(LastFrame[Y1:Y2,X1:X2], cv2.COLOR_BGR2GRAY)
            GrayB = cv2.cvtColor(Frame[Y1:Y2,X1:X2], cv2.COLOR_BGR2GRAY)
            Flow = cv2.calcOpticalFlowFarneback(GrayA, GrayB, None, pyr_scale=0.5, levels=3, winsize=15,
                                                iterations=3, poly_n=5, poly_sigma=1.1, flags=0)

            Size = TargetW * TargetH
            #PVector[Class, 3] = numpy.mean(cv2.cartToPolar(Flow[..., 0], Flow[..., 1])[0])

            cv2.putText(Frame, str(numpy.round(Size, decimals=2)), (X1,Y1),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

            # Update Last Frame
    LastFrame = Frame.copy()
    cv2.imshow("Window", Frame)
    print(numpy.round(PVector, decimals=2))
    # We cut the frame

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Camera.release()
cv2.destroyAllWindows()