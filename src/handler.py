def handle_command(command_parts):

    if not command_parts:
        return "-ERR empty command\r\n"

    command = command_parts[0].upper()

    if command == "PING":
        return "+PONG\r\n"

    return "-ERR unknown command\r\n"