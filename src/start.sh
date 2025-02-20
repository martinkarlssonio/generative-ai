#!/bin/sh

# Function to clean up on exit
cleanup() {
    echo "Shutting down services..."
    pkill -f "uvicorn main:app"
    pkill -f "ollama serve"
    pkill -f "python visualization_vector.py"
    exit 0
}

# Trap SIGTERM and SIGINT signals to properly terminate processes
trap cleanup SIGTERM SIGINT

# Start FastAPI server
cd /fastapi/app
uvicorn main:app --host 0.0.0.0 --port 8010 &

# Start Ollama API server with GPU support in the background
OLLAMA_CUDA=1 CUDA_VISIBLE_DEVICES=0 /usr/local/bin/ollama serve &

# Start Knowledge Embedding Visualization Server
cd /ai/knowledge
python visualization_vector.py &

# Keep the script alive
wait