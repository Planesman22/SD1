import torch
import cv2

class ObjectDetection:
    def __init__(self):
        self.model = self.load_model()
        self.classes = self.model.names
        self.device = 'gpu'

    def load_model(self):
        model = torch.hub.load('model/ultralytics_yolov5_master', 'yolov5s', source='local', pretrained=True)
        return model

    def score_frame(self, frame):
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
        labels, cord = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
        return labels, cord

    def class_to_label(self, x):
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.2:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
        return frame

    def __call__(self):
        player = cv2.VideoCapture(0)  # 0 means read from local camera.
        while player.isOpened():
            ret, frame = player.read()
            assert ret
            results = self.score_frame(frame)
            frame = self.plot_boxes(results, frame)
            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        player.release()
        cv2.destroyAllWindows()

a = ObjectDetection()
a()