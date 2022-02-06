#!/bin/bash

set -e

TAG="vw-reservation:latest"

# Make a random name for this container so we can delete it later
NAME="VW_ID4_$(date +%s)"

# Build and run container
docker build -f Dockerfile . -t "$TAG"
docker run --name "$NAME" -e USERNAME -e PASSWORD -e PAGE_LOAD_TIMEOUT_SECONDS -e VERBOSE "$TAG"

# Pause before closing to show output
read -p "Press any key to close ..."

# Remove container when we're done
docker rm "$NAME"