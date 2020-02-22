FROM python:3.8-slim

ARG MODE
ENV MODE $MODE

ARG DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE $DJANGO_SETTINGS_MODULE

ARG POSTGRES_NAME
ENV POSTGRES_NAME $POSTGRES_NAME

ARG POSTGRES_USER
ENV POSTGRES_USER $POSTGRES_USER

ARG POSTGRES_PASSWORD
ENV POSTGRES_PASSWORD $POSTGRES_PASSWORD

ARG POSTGRES_HOST
ENV POSTGRES_HOST $POSTGRES_HOST

ARG POSTGRES_PORT
ENV POSTGRES_PORT $POSTGRES_PORT

ARG SENTRY_DSN
ENV SENTRY_DSN $SENTRY_DSN

WORKDIR /code

RUN apt-get update && apt-get install -y gcc && pip install pipenv
COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock
RUN if [ "$MODE" = "local" ] || [ "$MODE" = "testing" ] ; then pipenv install --ignore-pipfile --dev --system ; fi
RUN if [ "$MODE" = "dev" ] || [ "$MODE" = "qa" ] || [ "$MODE" = "prod" ] ; then pipenv install --ignore-pipfile --system && python manage.py collectstatic --noinput ; fi
RUN apt-get remove -y gcc && apt-get autoremove -y

COPY . /code
CMD ./startup-script.sh
