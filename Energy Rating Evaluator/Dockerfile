FROM python:3.10.15-bookworm

WORKDIR /code

RUN apt-get update && apt-get install -y wget unzip tesseract-ocr \
    && apt-get install -y chromium chromium-driver \
    && apt-get clean

COPY ./requirements.txt .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver
