# README

1) create kafka topic:

docker-compose up
docker exec -it kafka_kafka1_1 kafka-topics --zookeeper zookeeper:2181 --create --topic my-topic --partitions 1 --replication-factor 3

2) run : python k_producer.py -- get reddit data and produce it to kafka topic
3) run : python k_consumer.py -- get data from kafka topic and write timestamps to csv file
4) run : python k_logs.py -- read csv file and draw graphic for latency of message processing -- save picture

for experiment : 

docker exec -it kafka_kafka1_1 kafka-topics --zookeeper zookeeper:2181 --create --topic my-topic2 --partitions 2 --replication-factor 3

docker exec -it kafka_kafka1_1 kafka-topics --zookeeper zookeeper:2181 --create --topic my-topic10 --partitions 10 --replication-factor 3


to experiment with different num of consumers/producers we should run k_consumer.py/k_producer.py files in few different terminals
