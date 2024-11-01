FROM python:3.10.15-bookworm

WORKDIR /code

RUN apt-get update && apt-get install -y \
    curl \
    tesseract-ocr \
    && apt-get clean

COPY . .

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["streamlit", "run", "main.py"]
