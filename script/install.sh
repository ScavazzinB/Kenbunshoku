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

# Check for Python 3
if ! command_exists python3; then
    echo "Error: Python 3 is not installed or not in the PATH."
    echo "Installing Python 3..."
    install_package python3
fi

# Check for pip
if ! command_exists pip3; then
    echo "Error: pip is not installed or not in the PATH."
    echo "Installing pip..."
    install_package python3-pip
fi

# Create virtual environment
echo "Creating virtual environment..."
if ! python3 -m venv "${PROJECT_DIR}/venv"; then
    echo "Error: Failed to create virtual environment."
    exit 1
fi

# Set permissions for the virtual environment directory
chmod -R 755 "${PROJECT_DIR}/venv"

# Activate virtual environment
echo "Activating virtual environment..."
if ! source "${PROJECT_DIR}/venv/bin/activate"; then
    echo "Error: Failed to activate virtual environment."
    exit 1
fi

# Check for requirements.txt
if [ ! -f "${PROJECT_DIR}/requirements.txt" ]; then
    echo "Error: requirements.txt not found."
    deactivate
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
if ! pip install -r "${PROJECT_DIR}/requirements.txt"; then
    echo "Error: Failed to install dependencies."
    deactivate
    exit 1
fi

# Set permissions for the logs directory and log file
LOG_DIR="${PROJECT_DIR}/Kenbunshoku/logs"
LOG_FILE="${LOG_DIR}/project.log"
mkdir -p "${LOG_DIR}"
touch "${LOG_FILE}"
chmod 755 "${LOG_DIR}"
chmod 644 "${LOG_FILE}"

echo "Installation complete. To activate the environment, use:"
echo "source ${PROJECT_DIR}/venv/bin/activate"