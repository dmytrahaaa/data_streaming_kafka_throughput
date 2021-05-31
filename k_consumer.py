from confluent_kafka import Consumer
import pandas as pd
import time

c = Consumer({
    'bootstrap.servers': 'localhost:9091,localhost:9092,localhost:9093',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})
c.subscribe(['my-topic']) # ['my-topic','my-topic2','my-topic10']

while True:
    msg = c.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    print('Received message: {}'.format(msg.value().decode('utf-8')))
    time.sleep(1)
    out = time.time()
    pd.DataFrame([[msg.timestamp()[1]/1000, out]]).to_csv('consumer_timestamps.csv', index=False, mode='a', header=False)
c.close()
