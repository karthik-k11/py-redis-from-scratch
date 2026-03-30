from store import set_key, get_key

def handle_command(command_parts):

    if not command_parts:
        return "-ERR empty command\r\n"

    command = command_parts[0].upper()

    ##PING
    if command == "PING":
        return "+PONG\r\n"

    ##SET key value [EX seconds]
    elif command == "SET":
        if len(command_parts) < 3:
            return "-ERR wrong number of arguments for 'SET'\r\n"

        key = command_parts[1]
        value = command_parts[2]

        ttl = None

        ##Handle EX option
        if len(command_parts) >= 5:
            option = command_parts[3].upper()

            if option == "EX":
                try:
                    ttl = int(command_parts[4])
                except:
                    return "-ERR invalid TTL\r\n"

        set_key(key, value, ttl)

        return "+OK\r\n"

    ##GET key
    elif command == "GET":
        if len(command_parts) < 2:
            return "-ERR wrong number of arguments for 'GET'\r\n"

        key = command_parts[1]
        value = get_key(key)

        if value is None:
            return "$-1\r\n"

        return f"${len(value)}\r\n{value}\r\n"

    return "-ERR unknown command\r\n"