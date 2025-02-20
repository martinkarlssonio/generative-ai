#!/bin/bash

# Awaits until ollama is ready
/usr/local/bin/ollama serve & sleep 30

# Define the model name
MODEL_NAME="test_ai"

# Define the Modelfile location
PROMPT_FILE="/ai/Modelfile"

##### DOWNLOAD BASE MODEL #####
# Check if the file exists
if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "File $PROMPT_FILE does not exist."
  exit 1
fi

# Extract the model name from the file
echo "### Extracting base model"
MODEL=$(grep -oP '^FROM\s+\K\S+' "$PROMPT_FILE")
echo "### Model name: $MODEL"

# Check if a model name was found
if [[ -z "$MODEL" ]]; then
  echo "### No model name found in $PROMPT_FILE."
  exit 1
fi

# Execute the ollama pull command
echo "### Pulling model: $MODEL"
ollama pull "$MODEL"

# Create the model with the custom prompt
echo "### Creating model $MODEL_NAME based on file: $PROMPT_FILE"
ollama create "$MODEL_NAME" -f "$PROMPT_FILE"