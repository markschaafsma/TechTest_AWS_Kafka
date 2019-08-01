import json
import logging

from kafka import KafkaConsumer,KafkaProducer

logging.basicConfig(level=logging.INFO)

consumer = KafkaConsumer(bootstrap_servers="3.82.26.109:9092,18.207.229.227:9092",auto_offset_reset='earliest',enable_auto_commit=True,value_deserializer=lambda m: json.loads(m.decode('utf-8')))
#consumer = KafkaConsumer(bootstrap_servers="3.82.26.109:9092,3.89.42.105:9092",auto_offset_reset='earliest',enable_auto_commit=True,value_deserializer=lambda m: json.loads(m.decode('utf-8')))
#consumer = KafkaConsumer(bootstrap_servers="172.31.80.132:9092,172.31.39.5:9092,172.31.16.193:9092",auto_offset_reset='earliest',enable_auto_commit=True,value_deserializer=lambda m: json.loads(m.decode('utf-8')))

producer = KafkaProducer(bootstrap_servers="3.82.26.109:9092,18.207.229.227:9092",key_serializer=str.encode,acks='all')

#subscribing the topic

consumer.subscribe(['learnkafka'])
#consumer.subscribe(['demo'])

for msg in consumer:
	if(msg[6]["TICKER"] == 'AMZN'):
		print("Consumed Records from learnkafka",msg[6])
		try:
			response = producer.send('transformedrecord',key='keyused',value=msg[6])
			logging.info("Sending Records to Kafka Topic transformedrecord")
		except Exception as e:
			logging.error("Exception occurred", exc_info=True)			
			
#for msg in consumer:
#    if(msg[6]["PRICE"] >= 60):
#	    print("Consumed Records from demo",msg[6])
					
					