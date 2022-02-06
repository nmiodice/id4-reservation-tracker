$TAG="vw-reservation:latest"

# Make a random name for this container so we can delete it later
$NAME="VW_ID4_"+$(([DateTimeOffset](Get-Date)).ToUnixTimeSeconds())

# Build and run container
docker build -f Dockerfile . -t "$TAG"
docker run --name "$NAME" --env-file=.env "$TAG"

# Pause before closing to show output
Read-Host "Press any key to close ..."

# Remove container when we're done
docker rm "$NAME"