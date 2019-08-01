import json
import random
import datetime
import logging

from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)

producer = KafkaProducer(bootstrap_servers="3.82.26.109:9092,18.207.229.227:9092",key_serializer=str.encode,acks='all')
#producer = KafkaProducer(bootstrap_servers="3.82.26.109:9092,3.89.42.105:9092",key_serializer=str.encode,acks='all')
#producer = KafkaProducer(bootstrap_servers="172.31.80.132:9092,172.31.39.5:9092,172.31.16.193:9092",key_serializer=str.encode,acks='all')

def getReferrer():
	data = {}
	now = datetime.datetime.now()
	str_now = now.isoformat()
	data['EVENT_TIME'] = str_now
	data['TICKER'] = random.choice(['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV'])
	price = random.random() * 100
	data['PRICE'] = round(price, 2)
	return data

while True:
	data = json.dumps(getReferrer())
	logging.info("Received Sample Data")
	try:
		response = producer.send('learnkafka',key='keyused',value=data)
		logging.info("Sending Records to Kafka Topic learnkafka")
		#response = producer.send('demo',key='keyused',value=data)
		#logging.info("Sending Records to Kafka Topic demo")
	except Exception as e:
		logging.error("Exception occurred", exc_info=True)
						