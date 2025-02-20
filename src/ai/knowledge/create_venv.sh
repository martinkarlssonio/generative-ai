#!/bin/bash

# Set default environment name
ENV_NAME="venv"

# Check if a name argument is provided
if [ $# -gt 0 ]; then
    ENV_NAME=$1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed. Install it first."
    exit 1
fi

# Create a virtual environment
echo "Creating virtual environment: $ENV_NAME ..."
python3 -m venv "$ENV_NAME"

# Check if creation was successful
if [ ! -d "$ENV_NAME" ]; then
    echo "Error: Failed to create virtual environment."
    exit 1
fi

echo "Virtual environment '$ENV_NAME' created successfully."

# Activate the virtual environment
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    source "$ENV_NAME/bin/activate"
    echo "Activated virtual environment: $ENV_NAME"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source "$ENV_NAME/Scripts/activate"
    echo "Activated virtual environment: $ENV_NAME (Windows)"
else
    echo "Warning: Unable to auto-activate on this OS. Run 'source $ENV_NAME/bin/activate' manually."
fi

# Install dependencies if a requirements file is provided
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
fi

echo "Done. Activate with : source venv/bin/activate"