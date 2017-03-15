FROM ubuntu:xenial
ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

RUN apt-get update && apt-get -y dist-upgrade

RUN apt-get install -y software-properties-common wget
RUN add-apt-repository -y ppa:fkrull/deadsnakes

RUN wget -qO- https://deb.nodesource.com/setup_6.x | sudo bash -

RUN apt-get update
RUN apt-get install -y redis-server \
    python3.6 \
    nodejs \
    xvfb \
    openjdk-8-jre-headless \
    google-chrome-stable \

RUN npm i -g selenium-standalone && selenium-standalone install

ADD src /root/api

RUN pip3 install -r /root/api/requirements.txt

USER root

CMD /root/api/start.sh

EXPOSE 8000