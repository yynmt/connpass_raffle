FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libffi-dev \
    libsqlite3-dev \
    zlib1g-dev \
    bzip2 \
    openssl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./connpass_raffle /app

EXPOSE 5000

CMD ["python", "main.py"]