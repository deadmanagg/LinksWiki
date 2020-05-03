#!/bin/sh
echo 'ZookeeperProcessStart ' "$1" 

if [ "$1" = "Start" ]
then

    nohup /usr/local/Cellar/kafka/2.4.1/bin/zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties > logZookeeper.txt &
else
    /usr/local/Cellar/kafka/2.4.1/bin/zookeeper-server-stop 
fi
echo 'ZookeeperProcessEnd ' "$1"
