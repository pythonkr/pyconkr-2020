FROM python:3.7.6

ENV PYTHONUNBUFFERED 1
WORKDIR /config
ADD requirements.txt /config/
RUN pip install -r requirements.txt
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && apt-get install -y yarn 
RUN apt-get install -y gettext
COPY . /app
WORKDIR /app
ENTRYPOINT ["/app/docker-entrypoint.sh"]
