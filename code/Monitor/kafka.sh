#!/bin/sh
echo 'KafkaProcessStart'
nohup /usr/local/Cellar/kafka/2.4.1/bin/kafka-server-start /usr/local/etc/kafka/server.properties > logKafka.txt &
echo 'KafkaProcessEnd'
