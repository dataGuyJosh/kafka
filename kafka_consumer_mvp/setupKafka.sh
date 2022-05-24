#!/bin/bash -e
# Kill child jobs on EXIT
trap 'rm -fr kafka* __pycache__; jobs -p | xargs kill' EXIT
# create new venv
python3 -m venv kafkaenv
# activate venv
. kafkaenv/bin/activate
# install requirements
# a fresh venv comes with an old version of pip
# for some of these requirements to work we must upgrade pip in the venv
python3 -m pip install --upgrade pip
pip install -r requirements.txt

curl https://dlcdn.apache.org/kafka/3.1.0/kafka_2.13-3.1.0.tgz -o kafka.tgz
tar -xzf kafka.tgz
rm kafka.tgz
cd kafka_*/

# set working directory to this directory (formatted for Windows CLI)
K_LOG_DIRS="$(pwd)/kafka-logs"
Z_LOG_DIRS="$(pwd)/zookeeper-logs"

# enable topic deletion
echo 'delete.topic.enable=true' >> config/server.properties
# setup log directory
sed -i "s~\(^log.dirs=\)\(.*\)~\1$K_LOG_DIRS~" config/server.properties
sed -i "s~\(^dataDir=\)\(.*\)~\1$Z_LOG_DIRS~" config/zookeeper.properties

# Start the ZooKeeper service
# Note: Soon, ZooKeeper will no longer be required by Apache Kafka.
bin/zookeeper-server-start.sh config/zookeeper.properties &

# Zookeeper has a session expiry time of 18000ms. 
# It needs this time to declare the old session dead. 
# If the Kafka broker is brought up before this happens, 
# the broker shuts down with "Error while creating ephemeral at /broker/ids/1, node already exists"
sleep 20

# Start the Kafka broker service
bin/kafka-server-start.sh config/server.properties &

sleep 5

# Delete Existing Topic ("|| true" lets this script continue if the topic did not exist)
bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic foo-topic,bar-topic,baz-topic || true

# Wait for topic to delete (depends on topic size)
sleep 20

# Create Kafka Topics
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic foo-topic
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic bar-topic
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic baz-topic

cd ..

sleep 10

read -rsn1 -p"Press any key to exit..."