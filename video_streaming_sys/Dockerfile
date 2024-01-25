# Use a base image with Python and OpenCv
FROM python:3.8-slim

# Use the official OpenCV base image
FROM opencv:4.5.3

# Set the working directory
WORKDIR /app


# Copy your Python script to the container
COPY script.py /app


# Install required dependencies
RUN pip install opencv-python-headless


# Run your Python script
CMD ["python", "script.py"]