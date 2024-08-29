# scr/config.py

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
PORT = 999

# Logging settings
LOG_DIR = 'logs'  # Directory to save log files