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

        command = ["SET", key, value]
        if ttl is not None:
            command += ["EX", str(ttl)]

        append_to_aof(command)


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

        if keys_to_delete:
            save_to_disk()


def save_to_disk():
    data = {
        "store": store,
        "expiry": expiry
    }

    with open("dump.json", "w") as f:
        json.dump(data, f)

def load_from_disk():
    global store, expiry

    try:
        with open("dump.json", "r") as f:
            data = json.load(f)

            store = data.get("store", {})
            expiry = data.get("expiry", {})

            print("[LOAD] Data loaded from disk")

    except FileNotFoundError:
        print("[LOAD] No dump file found, starting fresh")

def append_to_aof(command_parts):
    with open("aof.log", "a") as f:
        line = " ".join(command_parts)
        f.write(line + "\n")

def load_aof():
    global store, expiry

    try:
        with open("aof.log", "r") as f:
            for line in f:
                parts = line.strip().split()

                if not parts:
                    continue

                cmd = parts[0].upper()

                if cmd == "SET":
                    key = parts[1]
                    value = parts[2]

                    ttl = None
                    if len(parts) >= 5 and parts[3] == "EX":
                        ttl = int(parts[4])

                    store[key] = value
                    if ttl:
                        expiry[key] = time.time() + ttl

        print("[AOF] Loaded commands from log")

    except FileNotFoundError:
        print("[AOF] No log file found")