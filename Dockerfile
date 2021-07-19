# set the base image
FROM python:3.9

# File Author / Maintainer
MAINTAINER Timothy

#add project files to the usr/src/app folder
ADD . /usr/src/app

#set directoty where CMD will execute
WORKDIR /usr/src/app

COPY requirements.txt ./

# Get pip to download and install requirements:
RUN pip install --no-cache-dir -r requirements.txt
# Expose ports
EXPOSE 8000
# default command to execute
CMD exec gunicorn business.wsgi:application --bind 0.0.0.0:8000 --workers 1
#RUN python manage.py rqworker default

#docker build -t business .
#https://alibaba-cloud.medium.com/how-to-deploy-a-django-application-with-docker-9514be542909