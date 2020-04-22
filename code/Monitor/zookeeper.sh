#!/bin/sh
echo 'ZookeeperProcessStart'
nohup /usr/local/Cellar/kafka/2.4.1/bin/zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties > logZookeeper.txt &
echo 'ZookeeperProcessEnd'
