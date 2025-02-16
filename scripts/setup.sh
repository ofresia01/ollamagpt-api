#!/bin/sh

# Create the virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activate the virtual environment
case "$(uname)" in
    Darwin*|Linux*)
        source venv/bin/activate
        ;;
    MINGW*|MSYS*)
        source venv/Scripts/activate
        ;;
    *)
        echo "Unsupported OS"
        exit 1
        ;;
esac

# Install the dependencies if they are not already installed
pip install --upgrade pip
pip install -r requirements.txt