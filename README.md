# Kenbunshoku - Surveillance System

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Description

**Kenbunshoku** is a surveillance system that uses a webcam to detect motion and record video. It also provides a web interface to stream the video feed in real-time.

## Features

- Motion detection
- Video recording
- Real-time web streaming
- Configurable settings

## Installation

### Prerequisites

Ensure you have the following installed on your system:

- Python 3
- pip
- lsof

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/kenbunshoku.git
    cd kenbunshoku
    ```

2. Run the installation script:
    ```bash
    ./script/install.sh
    ```

## Usage

1. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```

2. Run the main program:
    ```bash
    ./script/run.sh
    ```

3. Open your web browser and navigate to `http://localhost:5000` to view the video feed.

## Configuration

You can configure the system by editing the `src/config.py` file. Here are the available settings:

```python
### Camera settings ####

# ID of the webcam to use
WEBCAM_ID = 0
# Resolution of the camera (width, height)
CAMERA_RESOLUTION = (640, 480)
# Frames per second for the camera
CAMERA_FPS = 30

#### Motion detection settings ####

# Pixel change sensitivity: Lower = more sensitive, Higher = less sensitive
MOTION_THRESHOLD = 25
# Number of changed areas to trigger detection: Lower = more sensitive, Higher = less sensitive
MOTION_SENSITIVITY = 5

#### Video recording settings ####

# Directory to save recorded videos
VIDEO_DIR = 'videos'
# Time to record before motion is detected (in seconds)
PRE_RECORD_TIME = 5
# Time to continue recording after motion stops (in seconds)
POST_RECORD_TIME = 5

#### Web streaming settings ####

# Port for the web server
PORT = 5000

# Logging settings
LOG_DIR = 'logs'  # Directory to save log files
