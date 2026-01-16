import time
import asyncio
async def f():
    time.sleep(1)
    print("inside f")
    
    
async def g():
    result = await f();
    return result;

asyncio.run(g())