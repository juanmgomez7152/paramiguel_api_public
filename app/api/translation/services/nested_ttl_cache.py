from cachetools import TTLCache

class NestedTTLCache:
    def __init__(self, ttl=3600, maxsize=100):
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def __getitem__(self, message):
        if message not in self.cache:
            self.cache[message] = {}
        return self.cache[message]

    def __setitem__(self, message, value):
        self.cache[message] = value
    
    def clear(self):
        self.cache.clear()