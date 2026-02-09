FROM ubuntu:22.04 as base
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /code
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    build-essential \
    ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH="src"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /code/src
COPY assets/ /code/assets 

FROM base as discord_bot
WORKDIR /code
CMD ["python3", "src/discord_bot/main.py"]

FROM base as escudo_de_mestre
WORKDIR /code
EXPOSE 8501
CMD ["streamlit", "run", "src/escudo_de_mestre/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
