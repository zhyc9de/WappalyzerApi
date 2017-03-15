FROM python:3

RUN cd /tmp && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && \
    apt-get -f -y install

RUN curl --silent --location https://rpm.nodesource.com/setup_6.x | bash -
RUN add-apt-repository -y ppa:openjdk-r/ppa

RUN apt-get update
RUN apt-get install -y redis-server nodejs openjdk-8-jre-headless

RUN npm install selenium-standalone@latest -g

ADD src /root/api

CMD /root/api/start.sh

EXPOSE 8000