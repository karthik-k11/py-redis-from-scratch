import time

store = {}
expiry = {}


def set_key(key, value, ttl=None):
    store[key] = value

    if ttl is not None:
        expiry_time = time.time() + int(ttl)
        expiry[key] = expiry_time
        print(f"[DEBUG] Expiry set: {key} expires at {expiry_time}")
    else:
        expiry.pop(key, None)


def get_key(key):
    if key in expiry:
        current_time = time.time()

        if current_time >= expiry[key]:
            store.pop(key, None)
            expiry.pop(key, None)
            return None

    return store.get(key)