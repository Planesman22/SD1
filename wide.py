import subprocess

subprocess.run("libcamera-vid -t 0 --inline -o udp://192.168.2.10:5000")