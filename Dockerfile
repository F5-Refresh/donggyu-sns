FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /var/www/sns

COPY requirements.txt /var/www/sns

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /var/www/sns