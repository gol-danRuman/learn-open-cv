FROM python:3.9-slim

# Install dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev && \
    pip install --no-cache-dir opencv-python-headless && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install face_recognition
RUN pip install --no-cache-dir face_recognition

# Install dlib
RUN apt-get update && apt-get install -y \
    libusb-1.0-0-dev && \
    pip install --no-cache-dir dlib && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install uvicorn and FastAPI
RUN pip install --no-cache-dir uvicorn fastapi

# Install NumPy
RUN pip install --no-cache-dir numpy

# Verify the Python version
RUN python --version



# Set the working directory to $APP_USER_HOME
WORKDIR $APP_USER_HOME

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install the Python dependencies on the virtual environment
RUN python3 -m pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt




#
COPY . .

#
CMD ["uvicorn", "fast_api_main:app", "--host", "0.0.0.0", "--port", "8000"]