FROM python:3.12.3-slim

WORKDIR /schedule_parser/

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt 

RUN apt-get update && apt-get install -y wget \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && apt-get clean
    
COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "alembic upgrade head && python -m src.main"]
