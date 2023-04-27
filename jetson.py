import cv2
import numpy
import socket
import struct
import subprocess
import torch

YoloModel = torch.hub.load('ultralytics/yolov5', 'yolov5s')
SelfIP = "192.168.2.10"  # Replace with the IP address of the NVIDIA Jetson AGX Xavier
Port = 5000
Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Socket.bind((SelfIP, Port))


