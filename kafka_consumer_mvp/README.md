# What does this do?
words here

## Kafka Stuff
```bash
# List all topics
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
# Get topic usage details
bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic test-topic --describe
# Read events from a topic
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test-topic --from-beginning
```

# URLs
Apache Kafka Quickstart

https://kafka.apache.org/quickstart

Basic Kafka Producer/Consumer Code

https://stackoverflow.com/questions/30391110/rest-api-for-kafka

Confluent Playlist

https://developer.confluent.io/learn-kafka/apache-kafka/events/

Youtube Playlist (same as above)

https://youtube.com/playlist?list=PLa7VYi0yPIH0KbnJQcMv5N9iW8HkZHztH