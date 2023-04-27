import cv2
import gi
import numpy as np
import sys
import torch

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Load YOLOv5 model
YoloModel = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Initialize GStreamer
Gst.init(None)

# Replace with the port number you used in the Raspberry Pi command
Port = 5000

# Create GStreamer pipeline
VideoPipelineConfig = f'udpsrc port={Port} caps="application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264" ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink'
VideoPipeline = Gst.parse_launch(VideoPipelineConfig)

# Get the appsink element and configure it
Sink = VideoPipeline.get_by_name('appsink0')
Sink.set_property('emit-signals', True)
Sink.set_property('sync', False)

# Callback function to process each frame
def processFrame(Sink):
    NewFrame = Sink.emit('pull-sample')
    if NewFrame:
        # Get the frame data as a numpy array
        Buffer = NewFrame.get_buffer()
        Success, Mapinfo = NewFrame.map(Gst.MapFlags.READ)

        # Decode the frame data using OpenCV
        frame = cv2.imdecode(np.frombuffer(Mapinfo.data, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Run YOLOv5 on the frame
        results = YoloModel(frame)

        # Display the received frame
        cv2.imshow('Received Video', frame)

        # Exit if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            VideoPipeline.set_state(Gst.State.NULL)
            sys.exit(0)

    return Gst.FlowReturn.OK

# Connect the callback function to the appsink
Sink.connect('new-sample', NewFrame)

# Start the GStreamer pipeline
VideoPipeline.set_state(Gst.State.PLAYING)

# Run the GLib main loop
Thread = GLib.MainLoop()
try:
    Thread.run()
except KeyboardInterrupt:
    VideoPipeline.set_state(Gst.State.NULL)
    Thread.quit()
