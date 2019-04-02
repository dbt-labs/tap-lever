
CACHE = {}

def add(key, val):
    CACHE[key] = val

def get(key):
    return CACHE.get(key)
