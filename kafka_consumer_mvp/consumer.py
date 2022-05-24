from aiokafka import AIOKafkaConsumer
from consumer_variables import *
import aiohttp # cannot use "requests" asychronously
import asyncio
import pyodbc

async def consume():
    global message_queue
    consumer = AIOKafkaConsumer(
        *TOPICS,
        bootstrap_servers=BOOTSTRAP_SERVER,
        group_id=GROUP_ID,                  # Consumer must be in a group to commit
        enable_auto_commit=True,            # We WANT to auto commit, as this keeps track of where we left off in a given topic
        auto_offset_reset="earliest")       # If committed offset not found, start from beginning
    
    # Get cluster layout and join group
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.offset, msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
            asyncio.create_task(publish_messages(msg))
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


# Send message offset and contents as post request to https://httpbin.org/post and print response
# FOR TESTING PURPOSES ONLY
async def send_messages():
    global message_queue
    async with aiohttp.ClientSession() as session:
        while len(message_queue):
            print("Queue Size: ",len(message_queue))
            msg = message_queue.popleft()
            async with session.post('https://httpbin.org/post', json = {msg.offset:msg.value.decode('utf-8')}) as resp:
                result = await resp.json()
                print(result['data'])


# Publish messages to database
async def publish_messages(msg):
    db=pyodbc.connect(DSN).cursor()
    query = "INSERT INTO [dbo].[batch_load_details] (targeturl,serverid,end_batch) VALUES (?,?,?)"
    target_url,service_id=str(msg.value(),'UTF-8').split()
    try:
        db.execute(query, target_url, service_id, '99')
        db.commit()
        db.close()
    except Exception as e:
        print(repr(e))


asyncio.run(consume())