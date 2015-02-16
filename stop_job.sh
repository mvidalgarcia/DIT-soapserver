#!/bin/bash
echo 'Killing places-server ...'
screen -S soap -X quit
echo 'Killing collector ...'
screen -S collector -X quit

