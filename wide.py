import cv2
import numpy as np
import socket
import struct
import sys
import time

# Configure the UDP socket
local_ip = "192.168.137.10"
local_port = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Configure the OpenCV VideoCapture object
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open the video stream.")
    sys.exit()

try:
    while True:
        # Capture the video frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame from video stream.")
            break

        # Resize
        frame = cv2.resize(frame, (320,240))

        # Encode the frame as a JPEG image
        result, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])

        if not result:
            print("Error: Could not encode the frame.")
            break

        # Send the encoded frame using the UDP socket
        data = buffer.tostring()
        sock.sendto(data, (local_ip, local_port))
        time.sleep(1)
finally:
    # Clean up the resources
    cap.release()
    sock.close()
    cv2.destroyAllWindows()
