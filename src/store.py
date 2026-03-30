import time

store = {}       
expiry = {}      


def set_key(key, value, ttl=None):
    store[key] = value

    if ttl is not None:
        expiry[key] = time.time() + ttl
    elif key in expiry:
        del expiry[key]


def get_key(key):
    ##Check expiry
    if key in expiry:
        if time.time() > expiry[key]:
            del store[key]
            del expiry[key]
            return None

    return store.get(key)