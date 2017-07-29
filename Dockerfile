FROM phusion/baseimage:0.9.19
MAINTAINER github.com/skylord123/xeoma-mqtt

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python-pip python-dev build-essential libffi-dev libssl-dev

ADD https://bootstrap.pypa.io/get-pip.py /tmp/get-pip.py
RUN cat /tmp/get-pip.py | python
RUN pip install paho-mqtt
RUN pip install python-etcd
RUN pip install flask

VOLUME [ "/config" ]

ADD xeoma-mqtt.py /usr/sbin/xeoma-mqtt.py

# add xeoma-mqtt.sh script to run as a service
RUN mkdir /etc/service/xeoma-mqtt
ADD xeoma-mqtt.sh /etc/service/xeoma-mqtt/run
RUN chmod +x /etc/service/xeoma-mqtt/run

EXPOSE 5000

#CMD [ "/usr/bin/python", "/usr/sbin/xeoma-mqtt.py" ]
