#!/bin/bash

export PYTHONPATH=src

# Set the default model
DEFAULT_MODEL="deepseek-r1:1.5b"

# Use the provided model or the default model
MODEL=${1:-$DEFAULT_MODEL}

# Set the environment variable for the model name
export OLLAMA_MODEL=$MODEL

# Function to clean up background processes
cleanup() {
    if [ -n "$OLLAMA_PID" ] && ps -p $OLLAMA_PID > /dev/null; then
        echo "Stopping Ollama process..."
        kill $OLLAMA_PID
        wait $OLLAMA_PID
        echo "Ollama process stopped."
    else
        echo "Ollama process already stopped or PID not set."
    fi

    if [ -n "$PROMETHEUS_PID" ] && ps -p $PROMETHEUS_PID > /dev/null; then
        echo "Stopping Prometheus process..."
        kill $PROMETHEUS_PID
        wait $PROMETHEUS_PID
        echo "Prometheus process stopped."
    else
        echo "Prometheus process already stopped or PID not set."
    fi
}

# Set trap to catch termination signals and clean up
trap cleanup EXIT

# Run the Ollama command in a separate process
ollama run $MODEL &
OLLAMA_PID=$!
echo "Ollama process started with PID $OLLAMA_PID"

# Check if Prometheus should be started
START_PROMETHEUS=${2:-true}
if [ "$START_PROMETHEUS" = true ]; then
    # Run the Prometheus server in a separate process
    prometheus --config.file="d:/repositories/chatbot-experimenting/prometheus.yml" &
    PROMETHEUS_PID=$!
    echo "Prometheus process started with PID $PROMETHEUS_PID"
fi

# Start the FastAPI server using Uvicorn
uvicorn src.app.main:app --reload