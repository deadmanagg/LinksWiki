#!/bin/sh
echo 'KafkaProcessStart' "$1" 
if [ "$1" = "Start" ]
then
    nohup /usr/local/Cellar/kafka/2.4.1/bin/kafka-server-start /usr/local/etc/kafka/server.properties > logKafka.txt &
else
    /usr/local/Cellar/kafka/2.4.1/bin/kafka-server-stop 
fi

echo 'KafkaProcessEnd' "$1" 
