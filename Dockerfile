FROM python:3.10.5-slim-bullseye

ENV PORT=8000
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT

CMD [ "python", "./main.py" ]
