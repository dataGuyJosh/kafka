from aiokafka import AIOKafkaProducer
from global_variables import *
import asyncio
import json


async def send_one():
    producer = AIOKafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVER)
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait(INPUT_TOPIC,json.dumps({"target_url":TARGET_URL,"serviceid":"32434"}).encode('utf-8'))
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

asyncio.run(send_one())