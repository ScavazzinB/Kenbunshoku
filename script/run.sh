#!/bin/bash

# Path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Function to install a package using the available package manager
install_package() {
    if command_exists apt-get; then
        sudo apt-get update && sudo apt-get install -y "$1"
    elif command_exists dnf; then
        sudo dnf install -y "$1"
    elif command_exists yum; then
        sudo yum install -y "$1"
    elif command_exists zypper; then
        sudo zypper install -y "$1"
    else
        echo "Error: No compatible package manager found (apt, dnf, yum, zypper)."
        exit 1
    fi
}

# Check for lsof
if ! command_exists lsof; then
    echo "Error: lsof is not installed or not in the PATH."
    echo "Installing lsof..."
    install_package lsof
fi

# Check if virtual environment exists
if [ ! -d "${PROJECT_DIR}/venv" ]; then
    echo "Error: Virtual environment does not exist. Please run install.sh first."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
if ! source "${PROJECT_DIR}/venv/bin/activate"; then
    echo "Error: Failed to activate virtual environment."
    exit 1
fi

# Check for main.py
if [ ! -f "${PROJECT_DIR}/src/main.py" ]; then
    echo "Error: main.py not found."
    deactivate
    exit 1
fi

# Check for config.py
if [ ! -f "${PROJECT_DIR}/src/config.py" ]; then
    echo "Error: config.py not found."
    deactivate
    exit 1
fi

# Extract port from config.py
PORT=$(grep -oP 'PORT\s*=\s*\K[0-9]+' "${PROJECT_DIR}/src/config.py")
if [ -z "$PORT" ]; then
    echo "Error: Unable to extract port from config.py."
    deactivate
    exit 1
fi

# Check if port is already in use
if lsof -i:"$PORT" &> /dev/null; then
    echo "Error: Port $PORT is already in use by another service."
    deactivate
    exit 1
fi

# Check if main.py has execution permissions
if [ ! -x "${PROJECT_DIR}/src/main.py" ]; then
    echo "Setting execution permissions for main.py..."
    chmod +x "${PROJECT_DIR}/src/main.py"
fi

# Run the main program
echo "Running the main program..."
if ! python "${PROJECT_DIR}/src/main.py"; then
    echo "Error: Failed to run the main program."
    deactivate
    exit 1
fi

deactivate