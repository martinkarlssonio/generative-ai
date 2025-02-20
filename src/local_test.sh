#!/bin/bash

# Variables
DOCKER_IMAGE="dataplatform-genai:local"
DOCKER_CONTAINER="dataplatform-genai-container"
LOCAL_PORT=8010
CONTAINER_PORT=8010
DOCKERFILE_PATH="./Dockerfile"

# Ensure Docker is running
if ! docker info >/dev/null 2>&1; then
  echo "Docker is not running. Please start Docker and try again."
  exit 1
fi

# Step 1: Build the Docker Image
echo "Building the Docker image..."
if ! docker build -t "$DOCKER_IMAGE" -f "$DOCKERFILE_PATH" .; then
  echo "Failed to build the Docker image. Please check the Dockerfile."
  exit 1
fi
echo "Docker image built successfully: $DOCKER_IMAGE"

# Step 2: Run the Docker Container
echo "Running the Docker container..."
if docker ps | grep -q "$DOCKER_CONTAINER"; then
  echo "A container with the name $DOCKER_CONTAINER is already running. Stopping it..."
  docker stop "$DOCKER_CONTAINER" >/dev/null
fi

if docker ps -a | grep -q "$DOCKER_CONTAINER"; then
  echo "Removing the existing container with the same name..."
  docker rm "$DOCKER_CONTAINER" >/dev/null
fi

if ! docker run -d --name "$DOCKER_CONTAINER" -p "$LOCAL_PORT:$CONTAINER_PORT" "$DOCKER_IMAGE"; then
  echo "Failed to run the Docker container. Please check the logs."
  exit 1
fi
echo "Docker container is running at http://localhost:$LOCAL_PORT"

# Step 3: Test the Container
echo "Testing the container..."
sleep 5  # Wait for the container to initialize

if curl -s "http://localhost:$LOCAL_PORT" | grep -q "Welcome to test Digital Platform"; then
  echo "Container is working as expected!"
else
  echo "Container test failed. Please check the logs and try again."
  docker logs "$DOCKER_CONTAINER"
  exit 1
fi

# Step 4: Cleanup Option
read -p "Do you want to stop and remove the container? (y/N): " cleanup
if [[ "$cleanup" =~ ^[Yy]$ ]]; then
  echo "Stopping and removing the container..."
  docker stop "$DOCKER_CONTAINER" >/dev/null
  docker rm "$DOCKER_CONTAINER" >/dev/null
  echo "Cleanup completed."
else
  echo "Container is still running at http://localhost:$LOCAL_PORT"
fi
