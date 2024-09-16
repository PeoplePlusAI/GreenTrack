FROM ubuntu:22.04

ENV TZ=Asia/Kolkata
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tesseract-ocr \
    firefox

WORKDIR /code

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt
