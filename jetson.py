import cv2
import gi
import numpy as np
import sys
import torch

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Initialize GStreamer
Gst.init(None)

# Replace with the port number you used in the Raspberry Pi command
port = 5000

# Create GStreamer pipeline
pipeline_str = f'udpsrc port={port} caps="application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264" ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink'
pipeline = Gst.parse_launch(pipeline_str)

# Get the appsink element and configure it
sink = pipeline.get_by_name('appsink0')
sink.set_property('emit-signals', True)
sink.set_property('sync', False)

# Callback function to process each frame
def new_sample(sink):
    sample = sink.emit('pull-sample')
    if sample:
        # Get the frame data as a numpy array
        buf = sample.get_buffer()
        result, mapinfo = buf.map(Gst.MapFlags.READ)

        # Decode the frame data using OpenCV
        frame = cv2.imdecode(np.frombuffer(mapinfo.data, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Run YOLOv5 on the frame
        results = model(frame)

        # Extract the feature probability vector
        # You can access the class probabilities, bounding box coordinates, and other information from the 'results' object

        # Perform OpenCV processing to find the object's screen velocity and size
        # Add your OpenCV processing code here

        # Display the received frame
        cv2.imshow('Received Video', frame)

        # Exit if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pipeline.set_state(Gst.State.NULL)
            sys.exit(0)

    return Gst.FlowReturn.OK

# Connect the callback function to the appsink
sink.connect('new-sample', new_sample)

# Start the GStreamer pipeline
pipeline.set_state(Gst.State.PLAYING)

# Run the GLib main loop
main_loop = GLib.MainLoop()
try:
    main_loop.run()
except KeyboardInterrupt:
    pipeline.set_state(Gst.State.NULL)
    main_loop.quit()
