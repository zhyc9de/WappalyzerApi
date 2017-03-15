#!/usr/bin/env bash

DISPLAY=:1

nohup xvfb-run selenium-standalone start &
nohup python3 probe.py &
nohup python3 server.py &
