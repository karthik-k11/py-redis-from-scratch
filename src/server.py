import socket
import threading
from constants import HOST, PORT, BUFFER_SIZE
from handler import handle_command
from resp_parser import parse_resp
from store import cleanup_expired_keys, load_aof
import time

def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")

    buffer = ""

    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)

            if not data:
                print(f"[DISCONNECTED] {address}")
                break

            buffer += data.decode("utf-8")

            while True:
                command_parts, buffer = parse_resp(buffer)

                if command_parts is None:
                    break  # wait for full command

                response = handle_command(command_parts)
                client_socket.sendall(response.encode("utf-8"))

        except ConnectionResetError:
            print(f"[CLIENT CLOSED] {address}")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            break

    client_socket.close()

def expiry_worker():

    while True:
        cleanup_expired_keys()
        time.sleep(2)   

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen()

    load_aof()

    print(f"[STARTED] Server running on {HOST}:{PORT}")
    threading.Thread(target=expiry_worker, daemon=True).start()

    while True:
        client_socket, address = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, address)
        )

        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()