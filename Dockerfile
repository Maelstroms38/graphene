FROM amd64/python:3.7-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

#  install psycopg2
RUN apk update \
	&& apk add --update alpine-sdk \
	&& apk --no-cache --update add build-base \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && pip3 install pip -U \
	&& pip3 install setuptools -U \
    && apk add postgresql-dev \
    && pip3 install psycopg2 \
    && apk del build-deps


# install dependencies
COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python3 manage.py collectstatic --noinput
RUN python3 -m spacy download en_core_web_sm

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# run gunicorn
CMD gunicorn library.wsgi:application --bind 0.0.0.0:$PORT