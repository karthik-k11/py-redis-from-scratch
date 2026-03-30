import time

store = {}
expiry = {}


def set_key(key, value, ttl=None):
    store[key] = value

    if ttl is not None:
        expiry_time = time.time() + int(ttl)
        expiry[key] = expiry_time
        print(f"[DEBUG] Set expiry for {key} at {expiry_time}")
    else:
        expiry.pop(key, None)


def get_key(key):
    if key in expiry:
        current_time = time.time()
        print(f"[DEBUG] Checking expiry: now={current_time}, expiry={expiry[key]}")

        if current_time >= expiry[key]:
            print(f"[DEBUG] Key expired: {key}")
            store.pop(key, None)
            expiry.pop(key, None)
            return None

    return store.get(key)