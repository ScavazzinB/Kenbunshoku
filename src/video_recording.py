# src/video_recording.py
import cv2
import os
from datetime import datetime
from config import CAMERA_RESOLUTION, CAMERA_FPS
from logger import setup_logger

logger = setup_logger('video_recording')

def set_file_permissions(file_path):
    """Set read and write permissions for all users for a given file."""
    os.chmod(file_path, 0o666)

def init_video_writer(resolution, fps, output_path):
    """Initialize a VideoWriter object for video recording."""
    logger.info(f"Initializing video writer: {output_path}")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, resolution)

    # Set file permissions after creating the video file
    set_file_permissions(output_path)

    return writer

def write_frame(writer, frame):
    """Write a frame to the video file."""
    writer.write(frame)

def release_writer(writer):
    """Close and save the video file."""
    logger.info("Closing video writer")
    writer.release()