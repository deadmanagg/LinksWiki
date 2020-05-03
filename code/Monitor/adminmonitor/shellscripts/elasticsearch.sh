#!/bin/sh
echo 'ESrocessStart' "$1" 
if [ "$1" = "Start" ]
then
    nohup /usr/local/Cellar/elasticsearch/6.8.7/bin/elasticsearch > logES.txt &
else
    pkill -f elasticsearch
fi
echo 'ESProcessEnd' "$1" 
