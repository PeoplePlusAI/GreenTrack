FROM python:3.10.15-bookworm

WORKDIR /code

RUN apt-get update && apt-get install -y wget unzip tesseract-ocr && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm ./google-chrome-stable_current_amd64.deb && \
    apt-get clean

COPY ./requirements.txt .

RUN pip install --trusted-host pypi.python.org -r requirements.txt
