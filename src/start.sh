#!/usr/bin/env bash

nohup selenium-standalone start &
nohup python3 probe.py &
nohup python3 server.py &
