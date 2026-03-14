import os
import redis
import asyncio
import uvloop
import logging
from telethon import TelegramClient, events, connection, Button
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
logging.basicConfig(level=logging.WARNING)
API_ID = int(os.getenv("API_ID"))  
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
pool = redis.ConnectionPool(
    host='localhost', 
    port=6379, 
    db=0, 
    decode_responses=True,
    max_connections=100
)
r = redis.Redis(connection_pool=pool)
MAX_CONCURRENT_TASKS = 500
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
ABH = TelegramClient(
    "roullette", 
    API_ID, 
    API_HASH,
    connection=connection.ConnectionTcpFull,
    sequential_updates=False,
    auto_reconnect=True,
    connection_retries=None,
    flood_sleep_threshold=60 
)
