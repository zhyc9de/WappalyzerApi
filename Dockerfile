FROM selenium/standalone-chrome

RUN apt-get update && apt-get -y dist-upgrade

RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:fkrull/deadsnakes

RUN apt-get update
RUN apt-get install -y redis-server python3.6

ADD src /root/api

CMD /root/api/start.sh

EXPOSE 8000