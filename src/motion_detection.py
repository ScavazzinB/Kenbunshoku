# scr/motion_detection.py
import cv2
from config import MOTION_SENSITIVITY
from logger import setup_logger

logger = setup_logger('motion_detection')

def detect_motion(prev_frame, curr_frame, threshold=25):
    """Detect motion between two consecutive frames."""
    gray_prev = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    gray_curr = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray_prev, gray_curr)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = len(contours) > MOTION_SENSITIVITY
    if motion_detected:
        logger.info(f"Motion detected (contours: {len(contours)})")
    return motion_detected