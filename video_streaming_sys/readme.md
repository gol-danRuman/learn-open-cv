
A Python program using OpenCV to perform live video streaming inside a Docker container.

# Build the Docker image
> docker build -t video-streaming-container


# Run the Docker container
> docker run --privileged -v /dev/video0:/dev/video0 video-streaming-container


This example captures video from the default camera (/dev/video0), encodes it using the XVID codec, and saves it as an AVI file named output.avi.


> Reference:
    - https://www.linkedin.com/pulse/igniting-visual-connectivity-empower-live-video-streaming-kumar/
