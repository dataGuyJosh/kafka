from aiokafka import AIOKafkaConsumer
from global_variables import *
import aiohttp # cannot use "requests" asychronously
import asyncio
import pyodbc

async def consume():
    global message_queue
    consumer = AIOKafkaConsumer(
        *OUTPUT_TOPICS,
        bootstrap_servers=BOOTSTRAP_SERVER,
        # comment out group_id & enable_auto_commit to start reading from beginning of topic
        group_id=GROUP_ID,                  # Consumer must be in a group to commit
        enable_auto_commit=True,            # We WANT to auto commit, as this keeps track of where we left off in a given topic
        auto_offset_reset="earliest")       # If committed offset not found, start from beginning
    
    # Get cluster layout and join group
    print('Connecting to:',BOOTSTRAP_SERVER,'Topics:',OUTPUT_TOPICS)
    await consumer.start()
    print('Connected! Listening...')
    try:
        # Consume messages
        async for msg in consumer:
            # Message Details
            # print(msg.offset, msg.topic, msg.partition, msg.offset, msg.key, msg.timestamp)

            # Message Contents
            print(msg.value)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

asyncio.run(consume())