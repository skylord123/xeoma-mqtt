FROM ubuntu:14.04
MAINTAINER Skylar Sadlier "skylord123@gmail.com"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python-pip python-dev build-essential libffi-dev libssl-dev

ADD https://bootstrap.pypa.io/get-pip.py /tmp/get-pip.py
RUN cat /tmp/get-pip.py | python
RUN pip install paho-mqtt
RUN pip install python-etcd
RUN pip install flask

VOLUME [ "/config" ]
COPY config.ini.default /files/
# setup startup scripts
COPY 30_default_config_file.sh /etc/my_init.d/

ADD xeoma-mqtt.py /usr/sbin/xeoma-mqtt.py

EXPOSE 5000

CMD [ "/usr/bin/python", "/usr/sbin/xeoma-mqtt.py" ]
