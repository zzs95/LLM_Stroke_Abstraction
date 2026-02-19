#!/bin/bash

GPU_ID=0
PORT=11435
CONTAINER_NAME=ollama_gpu${GPU_ID}
MODEL_DIR=~/.ollama

docker run -d \
  --gpus "device=${GPU_ID}" \
  -v ${MODEL_DIR}:/root/.ollama \
  -p ${PORT}:11435 \
  --name ${CONTAINER_NAME} \
  --restart unless-stopped \
  ollama/ollama

echo "Ollama running on GPU ${GPU_ID} at http://localhost:${PORT}"