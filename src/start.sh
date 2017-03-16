#!/usr/bin/env bash

DISPLAY=:1

nohup redis-server /etc/redis/redis.conf &
sleep 1
nohup xvfb-run selenium-standalone start &
sleep 1
nohup python3 probe.py &
sleep 1
nohup python3 server.py &
