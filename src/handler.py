from store import store

def handle_command(command_parts):

    if not command_parts:
        return "-ERR empty command\r\n"

    command = command_parts[0].upper()

    ##PING
    if command == "PING":
        return "+PONG\r\n"

    ##SET key value
    elif command == "SET":
        if len(command_parts) < 3:
            return "-ERR wrong number of arguments for 'SET'\r\n"

        key = command_parts[1]
        value = command_parts[2]

        store[key] = value

        return "+OK\r\n"

    ##GET key
    elif command == "GET":
        if len(command_parts) < 2:
            return "-ERR wrong number of arguments for 'GET'\r\n"

        key = command_parts[1]

        if key in store:
            value = store[key]
            return f"${len(value)}\r\n{value}\r\n"   # RESP Bulk String

        return "$-1\r\n"   # NULL (Redis style)

    return "-ERR unknown command\r\n"