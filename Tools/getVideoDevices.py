import cv2

num_devices = 0

for i in range(10):
    cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
    if cap.isOpened():
        num_devices += 1
        cap.release()
    else:
        break

print(f"Number of available VideoCapture devices: {num_devices}")