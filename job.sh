#!/bin/bash
screen -S soap -d -m python3 run.py
sleep 3
cd gplaces
screen -S collector -d -m python3 schedule.py
