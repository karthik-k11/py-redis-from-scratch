import socket
import threading
from constants import HOST, PORT, BUFFER_SIZE
from handler import handle_command
from resp_parser import parse_resp


def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")

    buffer = ""

    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)

            if not data:
                print(f"[DISCONNECTED] {address}")
                break

            decoded_data = data.decode("utf-8")
            buffer += decoded_data

            print(f"[RAW BUFFER]\n{buffer}")

            ##Only process if we got full command
            if "\n" not in buffer:
                continue

            command_parts = parse_resp(buffer)

            print(f"[PARSED] {command_parts}")

            if not command_parts:
                continue

            response = handle_command(command_parts)

            client_socket.sendall(response.encode("utf-8"))

            buffer = ""  

        except Exception as e:
            print(f"[ERROR] {e}")
            break

    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen()

    print(f"[STARTED] Server running on {HOST}:{PORT}")

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