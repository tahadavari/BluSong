FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apt-get update

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py"]