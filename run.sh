#!/bin/bash

set -e

TAG="vw-reservation:latest"

docker build -f Dockerfile . -t "$TAG"
docker run -e USERNAME="$USERNAME" -e PASSWORD="$PASSWORD" "$TAG"
