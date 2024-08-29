# src/web_stream.py
import cv2
from multiprocessing import Process
from camera import Camera
from logger import global_logger as logger

global_frame = None
camera = None

def gen_frames():
    global global_frame
    while True:
        if global_frame is not None:
            ret, buffer = cv2.imencode('.jpg', global_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def update_frame(frame):
    global global_frame
    global_frame = frame

def start_streaming(camera):
    while True:
        frame = camera.capture_image()
        update_frame(frame)