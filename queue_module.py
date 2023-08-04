import asyncio
from ozon.main import parse

my_queue = asyncio.Queue()


async def process_requests():
    while not my_queue.empty():
        await asyncio.sleep(0.1)
        url, user_id = await my_queue.get()
        await asyncio.sleep(0.1)
        await parse(url, user_id)
        await asyncio.sleep(0.1)
        my_queue.task_done()
