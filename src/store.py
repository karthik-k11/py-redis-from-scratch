import time
import threading
import json

store = {}
expiry = {}

lock = threading.Lock()


def set_key(key, value, ttl=None):
    with lock:
        store[key] = value

        if ttl is not None:
            expiry[key] = time.time() + int(ttl)
        else:
            expiry.pop(key, None)


def get_key(key):
    with lock:
        if key in expiry:
            if time.time() >= expiry[key]:
                store.pop(key, None)
                expiry.pop(key, None)
                return None

        return store.get(key)


def cleanup_expired_keys():
    with lock:
        current_time = time.time()

        keys_to_delete = []

        for key, exp_time in expiry.items():
            if current_time >= exp_time:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            print(f"[CLEANUP] Removing expired key: {key}")
            store.pop(key, None)
            expiry.pop(key, None)