FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install Flask

COPY . .

CMD [ "python", "./app.py" ]
