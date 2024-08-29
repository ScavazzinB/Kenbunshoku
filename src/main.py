import cv2
from flask import Flask, render_template, Response
from config import PORT
from web_stream import gen_frames, update_frame
from logger import global_logger as logger
from camera import Camera
from object_detection import ObjectDetection

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    camera = Camera()
    object_detection = ObjectDetection()

    while True:
        frame = camera.get_frame()
        frame = object_detection.detect_objects(frame)
        update_frame(frame)


if __name__ == '__main__':
    from threading import Thread

    logger.info("Starting main thread...")
    # Start the main loop in a separate thread
    main_thread = Thread(target=main)
    main_thread.daemon = True
    main_thread.start()

    logger.info(f"Starting Flask app on port {PORT}...")
    # Run the Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)