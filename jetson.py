import gi
import sys

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Initialize GStreamer
Gst.init(None)

# Replace with the port number you used in the Raspberry Pi command
port = 5000

# Create GStreamer pipeline
pipeline_str = f'udpsrc port={port} caps="application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264" ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink'
pipeline = Gst.parse_launch(pipeline_str)

# Start the GStreamer pipeline
pipeline.set_state(Gst.State.PLAYING)

# Run the GLib main loop
main_loop = GLib.MainLoop()
try:
    main_loop.run()
except KeyboardInterrupt:
    pipeline.set_state(Gst.State.NULL)
    main_loop.quit()
