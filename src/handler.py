def handle_command(data: str) -> str:
    command = data.strip().upper()

    if command == "PING":
        return "+PONG\r\n"

    return "-ERR unknown command\r\n"