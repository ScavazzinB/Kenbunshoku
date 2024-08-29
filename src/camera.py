# src/camera.py
import cv2
from config import WEBCAM_ID, CAMERA_RESOLUTION
from logger import global_logger as logger, log_system_info

class Camera:
    def __init__(self):
        self.camera = self.init_camera()

    def init_camera(self):
        try:
            camera = cv2.VideoCapture(WEBCAM_ID)
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_RESOLUTION[0])
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_RESOLUTION[1])

            if not camera.isOpened():
                raise Exception("Could not open camera")

            logger.info('Camera initialized successfully.')
            log_system_info(logger)
            return camera
        except Exception as e:
            logger.error(f'Failed to initialize camera: {e}')
            log_system_info(logger)
            raise

    def capture_image(self):
        ret, frame = self.camera.read()
        if not ret:
            logger.error('Failed to capture image')
            return None
        return frame