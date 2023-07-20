FROM python:latest

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y \
    python3-dev\
    libpq-dev\
    gcc\
    libstdc++6 \
    postgresql-server-dev-all \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]
