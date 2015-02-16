#!/bin/bash
screen -S soap -dm bash -c ". venv/bin/activate; python3 run.py > places_server_$(date +%s).log 2>&1"
sleep 2 
cd gplaces
screen -S collector -dm bash -c ". ../venv/bin/activate; python3 collector.py > ../collector_$(date +%s).log 2>&1"
cd ..
