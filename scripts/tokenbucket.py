import asyncio
import time


class TokenBucket:
    def __init__(self, tokens, time_unit, forward_callback, drop_callback):
        """
        tokens: The number of tokens to add to the bucket per time_unit
        time_unit: The time unit in seconds
        forward_callback: The callback to call when a packet is forwarded
        drop_callback: The callback to call when a packet is dropped
        """
        self.tokens = tokens
        self.time_unit = time_unit
        self.forward_callback = forward_callback
        self.drop_callback = drop_callback
        self.bucket = tokens
        self.last_check = time.monotonic()
        self.lock = asyncio.Lock()
        
    
    def handle(self, packet):
        current = time.time()
        
        monotonic = time.monotonic()
        
        print("monotonic: ", monotonic)
        
        time_passed = current - self.last_check
        print("current time: ", current, "last check: ", self.last_check, "time passed: ", time_passed)
        
tb = TokenBucket(10, 1, lambda: print("forward"), lambda: print("drop"))
time.sleep(1)
tb.handle(1)