#!/bin/bash
screen -S soap -dm bash -c ". venv/bin/activate; python3 run.py"
sleep 2 
cd gplaces
screen -S collector -dm bash -c ". ../venv/bin/activate; python3 collector.py"
cd ..
