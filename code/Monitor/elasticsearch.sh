#!/bin/sh
echo 'ESrocessStart'
nohup /usr/local/Cellar/elasticsearch/6.8.7/bin/elasticsearch > logES.txt &
echo 'ESProcessEnd'
