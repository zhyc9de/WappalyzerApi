FROM ubuntu:xenial
ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

USER root

RUN apt-get update && apt-get -y dist-upgrade

RUN apt-get install -y wget

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list

RUN wget -qO- https://deb.nodesource.com/setup_6.x | bash -

RUN apt-get update
RUN apt-get install -y redis-server \
    python3.5 \
    nodejs \
    xvfb \
    openjdk-8-jre-headless \
    google-chrome-stable

RUN npm i -g selenium-standalone && selenium-standalone install

ADD src /root/api

RUN pip3 install -r /root/api/requirements.txt

RUN apt-get autoclean && apt-get clean && apt-get autoremove

RUN rm -rf /var/cache/apt/archives

CMD /root/api/start.sh

EXPOSE 8000