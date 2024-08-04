# Pull base image
FROM python:3.11-slim

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ghostscript \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libpoppler-cpp-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install OpenCV
RUN pip install opencv-python-headless

# Copy the wheel file into the container
COPY wheel_files/python3_ghostscript-0.5.0-py3-none-any.whl /code/wheel_files/

# Install dependencies
COPY ./requirementsv1.txt .
RUN pip install -r requirementsv1.txt

# Copy project
COPY . .