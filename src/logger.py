# src/logger.py
import logging
import psutil
import os


def setup_logger():
    logger = logging.getLogger('kenbunshoku')
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'kenbunshoku.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


global_logger = setup_logger()


def log_system_info(logger):
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    logger.info(f"CPU Usage: {cpu_percent}%")
    logger.info(f"Memory Usage: {memory.percent}%")
    logger.info(f"Disk Usage: {disk.percent}%")