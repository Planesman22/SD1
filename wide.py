import cv2
import socket
import subprocess
import time

TargetIP = "192.168.2.10"
Port = 5000
Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Try to get camera to work
while True:
    try:
        Cam = cv2.VideoCapture(0)
        if Cam.isOpened():
            break
        else:
            print("Cam not ready!")
            Cam.release()
            time.sleep(1)
    except:
        print("Cam error!")
        Cam.release()
        time.sleep(1)

# Setup FFMPeg
CamWidth = int(Cam.get(cv2.CAP_PROP_FRAME_WIDTH))
CamHeight = int(Cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
CamFPS = int(Cam.get(cv2.CAP_PROP_FPS))

print("Cam Width: "+str(CamWidth))
print("Cam Height: "+str(CamHeight))
print("Cam FPS: "+str(CamFPS))

ffmpeg_cmd = [
    'ffmpeg',
    '-f', 'rawvideo',
    '-pixel_format', 'bgr24',
    '-video_size', f'{CamWidth}x{CamFPS}',
    '-framerate', f'{CamFPS}',
    '-i', 'pipe:',
    '-an',
    '-c:v', 'libx265',
    '-preset', 'ultrafast',
    '-tune', 'zerolatency',
    '-f', 'hevc',
    'pipe:'
]

ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  bufsize=10 ** 8)

try:
    while True:
        # Capture the video frame
        Success, Frame = Cam.read()

        if not Success:
            print("Cam Problem!")
            break

        # Frame to FFMPEG
        ffmpeg_process.stdin.write(Frame.tobytes())

        # FFMPEG to Data
        ProcessedData = ffmpeg_process.stdout.read1(65536)

        if len(ProcessedData) == 0:
            print("FFMPEG Screwd up!")
            break

        # Go!
        Socket.sendto(ProcessedData, (TargetIP, Port))
finally:
    # Exit time
    Cam.release()
    Socket.close()
    ffmpeg_process.stdin.close()
    ffmpeg_process.stdout.close()
    ffmpeg_process.stderr.close()
    ffmpeg_process.terminate()
    cv2.destroyAllWindows()
