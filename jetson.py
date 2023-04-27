import cv2
import numpy as np
import socket
import struct

# Configure the UDP socket
local_ip = "192.168.137.10"
local_port = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((local_ip, local_port))

cv2.namedWindow('Received Video', cv2.WINDOW_NORMAL)

try:
    while True:
        # Receive the encoded frame from the sender
        data, addr = sock.recvfrom(65536)

        # Decode the received frame
        frame_data = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)

        if frame is not None:
            # Display the received frame
            cv2.imshow('Received Video', frame)

            # Exit if the user presses the 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:
    # Clean up the resources
    sock.close()
    cv2.destroyAllWindows()
