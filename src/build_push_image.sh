#!/bin/bash

# Variables
REGION="eu-north-1"
REPOSITORY_NAME="infrastructure-ecr"
REPO_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPOSITORY_NAME}"
TAG="dataplatform-genai-v1"

# Ensure Docker is running
if ! docker info >/dev/null 2>&1; then
  echo "Docker is not running. Please start Docker and try again."
  exit 1
fi

# Authenticate with ECR
echo "Authenticating with Amazon ECR..."
aws ecr get-login-password --region "${REGION}" | docker login --username AWS --password-stdin "${REPO_URI}"

# Build the Docker Image
echo "Building the Docker image..."
docker build -t "${REPO_URI}:${TAG}" .

# Push the Docker Image to ECR
echo "Pushing the Docker image to ECR..."
docker push "${REPO_URI}:${TAG}"

# Final Step: Confirm Success
echo "Docker image '${REPO_URI}:${TAG}' pushed successfully."
