FROM python:3.11.9-alpine3.20

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache firefox

WORKDIR /code

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
