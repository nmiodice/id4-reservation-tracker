#!/bin/bash

set -e

TAG="vw-reservation:latest"

docker build -f Dockerfile . -t "$TAG"
docker run -e USERNAME -e PASSWORD -e PAGE_LOAD_TIMEOUT_SECONDS "$TAG"
