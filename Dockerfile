FROM python:3.9
LABEL autor="ATLAS-NTS"
LABEL description="DJANGO APP"

WORKDIR /usr/src/helpers/
COPY . /usr/src/helpers/

RUN apt-get update

RUN echo "Y" | apt-get install alien
RUN echo "Y" | apt-get install gunicorn
# RUN echo "Y" | apt-get install memcached
RUN echo "Y" | apt-get install unixodbc
RUN echo "Y" | apt-get install unixodbc-dev
RUN echo "Y" | apt-get install cifs-utils

# RUN apt-get install libaio1

RUN echo "Y" | apt-get install python3-dev default-libmysqlclient-dev build-essential

RUN groupadd -r djuser && useradd -r -g djuser djuser
RUN apt-get update --allow-releaseinfo-change
# RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENV pip=pip3
ENV python=python3
ENV DJANGO_SETTINGS_MODULE=faq.settings
# ENV DJANGO_DEBUG=0
# ENV DJANGO_ALLOWED_HOSTS='*'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

USER djuser

EXPOSE 4307
