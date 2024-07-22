FROM --platform=linux/amd64 python:3.7.17-slim-bullseye

ENV PYTHONUNBUFFERED 1
WORKDIR /config
ADD requirements.txt /config/
RUN apt-get update
RUN apt-get install -y build-essential curl  postgresql-server-dev-13
RUN pip install -r requirements.txt
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && apt-get install -y yarn 
RUN apt-get install -y gettext
COPY . /app
WORKDIR /app
ENTRYPOINT ["/app/docker-entrypoint.sh"]
