FROM python:3.7-slim

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-dev \
        libxml2-dev \
        libxslt1-dev \
        libxslt-dev \
        libyajl2 \
        gcc && \
    rm -r /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install Flask && \
    apt-get autoremove -y && apt-get remove -y gcc

CMD [ "python", "./app.py" ]
