# src/main.py
from os import listdir
from os.path import isfile, join
import os
import re
from web_stream import start_streaming, gen_frames
from threading import Thread
from flask import Flask, render_template, Response
from config import PORT, VIDEO_DIR, PRE_RECORD_TIME, POST_RECORD_TIME
from config import CAMERA_RESOLUTION, CAMERA_FPS
from web_stream import update_frame
from logger import global_logger as logger
from camera import Camera
from motion_detection import MotionDetection
from video_recording import init_video_writer, write_frame, release_writer, set_file_permissions
from utils import get_video_path
from collections import deque
from datetime import datetime, timedelta
from multiprocessing import Process, Queue

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/logs')
def return_logs():
    video_dir = 'videos'  # Remplacez par le chemin de votre dossier de vidéos
    video_files = [f for f in listdir(video_dir) if isfile(join(video_dir, f))]

    # Stocker les noms des fichiers vidéo dans une variable globale
    global previous_video_files
    if 'previous_video_files' not in globals():
        previous_video_files = video_files

    new_videos = list(set(video_files) - set(previous_video_files))
    previous_video_files = video_files

    return "<br>".join(new_videos) if new_videos else "No new videos"
def run_flask_app():
    logger.info(f"Starting Flask app on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)

def record_video(queue):
    video_writer = None
    try:
        while True:
            timestamp, frame = queue.get()
            if video_writer is None:
                video_path = get_video_path(VIDEO_DIR)
                video_writer = init_video_writer(CAMERA_RESOLUTION, CAMERA_FPS, video_path)
            write_frame(video_writer, frame)
            if timestamp is None:  # End of recording signal
                break
    except Exception as e:
        logger.error(f"Error in video recording process: {e}")
    finally:
        if video_writer is not None:
            release_writer(video_writer)

def main():
    camera = Camera()
    streaming_thread = Thread(target=start_streaming, args=(camera,))
    streaming_thread.start()
    motion_detection = MotionDetection()

    prev_frame = None
    frames_buffer = deque(maxlen=PRE_RECORD_TIME * CAMERA_FPS)
    last_motion_time = None
    recording_process = None
    recording_queue = Queue()

    while True:
        curr_frame = camera.capture_image()
        if curr_frame is None:
            logger.error('Failed to capture image')
            continue
        update_frame(curr_frame)  # Update the stream with every captured frame
        frames_buffer.append((datetime.now(), curr_frame))
        if prev_frame is not None:
            motion_detected = motion_detection.detect_motion(prev_frame, curr_frame)
            if motion_detected:
                last_motion_time = datetime.now()
                if recording_process is None or not recording_process.is_alive():  # Start new recording process if not already recording
                    if recording_process is not None:  # Previous recording process ended, release resources
                        recording_process.join()
                        recording_queue.close()
                        recording_queue = Queue()
                    recording_process = Thread(target=record_video, args=(recording_queue,))
                    recording_process.start()
                    for _, frame in frames_buffer:  # Write pre-record frames
                        recording_queue.put((datetime.now(), frame))
                recording_queue.put((datetime.now(), curr_frame))
            elif recording_process is not None and datetime.now() - last_motion_time > timedelta(seconds=POST_RECORD_TIME):  # Check if post-record time has passed since last motion
                recording_queue.put((None, None))  # Send end of recording signal
                recording_process = None
        prev_frame = curr_frame

if __name__ == '__main__':
    logger.info("Starting main thread...")
    main_thread = Thread(target=main)
    main_thread.daemon = True
    main_thread.start()

    logger.info(f"Starting Flask app on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)