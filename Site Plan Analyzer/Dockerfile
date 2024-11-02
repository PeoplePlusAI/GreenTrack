FROM python:3.10.15-bookworm

WORKDIR /code

RUN apt-get update && apt-get install -y \
    curl \
    tesseract-ocr \
    && apt-get clean

COPY ./requirements.txt .

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

COPY ./app .

ENTRYPOINT ["streamlit", "run", "main.py"]
