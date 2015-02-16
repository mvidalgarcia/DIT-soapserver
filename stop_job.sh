#!/bin/bash
echo 'Killing places-server ...'
screen -S soap -p 0 -X stuff 
echo 'Killing collector ...'
screen -S collector -p 0 -X stuff 

