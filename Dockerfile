FROM python:3.7.3

ENV PYTHONUNBUFFERED 1
WORKDIR /config
COPY . /app
ADD requirements.txt /config/
RUN pip install -r requirements.txt

WORKDIR /app
ENTRYPOINT ["/app/docker-entrypoint.sh"]
