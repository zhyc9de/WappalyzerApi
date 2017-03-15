#!/usr/bin/env bash

pip3 install -U requirements.txt

nohup python3 probe.py &
python3 server.py
