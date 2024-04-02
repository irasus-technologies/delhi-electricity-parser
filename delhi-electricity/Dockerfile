ARG PYTHON_VERSION=3.12.2

FROM python:${PYTHON_VERSION}

MAINTAINER Anirudh Ramesh

WORKDIR /

RUN mkdir -p /goodenough

RUN \
    set -e \
\
    && apt update \
    && apt -y upgrade \
    && apt install -y cron \
    && echo ""

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY __init__.py /
RUN mkdir -p /parser/
COPY parser/ /parser/

# cron

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab


# Docker entrypoint

COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh
ENTRYPOINT /entrypoint.sh
