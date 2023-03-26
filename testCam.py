import cv2

VisionDevice = cv2.VideoCapture(0)  # 0 means read from local camera.
while VisionDevice.isOpened():
    ret, frame = VisionDevice.read()
    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

VisionDevice.release()
cv2.destroyAllWindows()