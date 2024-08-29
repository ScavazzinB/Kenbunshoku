# scr/video_recording.py
import cv2
import os
from datetime import datetime
from config import CAMERA_RESOLUTION, CAMERA_FPS
from logger import setup_logger

logger = setup_logger('video_recording')

def init_video_writer(resolution, fps, output_path):
    """Initialize a VideoWriter object for video recording."""
    logger.info(f"Initializing video writer: {output_path}")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, resolution)
    return writer

def write_frame(writer, frame):
    """Write a frame to the video file."""
    writer.write(frame)

def release_writer(writer):
    """Close and save the video file."""
    logger.info("Closing video writer")
    writer.release()