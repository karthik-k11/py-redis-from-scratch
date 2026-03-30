def parse_resp(data: str):

    data = data.replace("\r\n", "\n")

    raw_lines = data.split("\n")
    lines = [line for line in raw_lines if line.strip() != ""]

    if not lines:
        return None, data

    ##Non-RESP fallback
    if not lines[0].startswith("*"):
        return [lines[0].strip()], "\n".join(lines[1:])

    try:
        num_elements = int(lines[0][1:])
    except:
        return None, data

    expected_lines = 1 + num_elements * 2

    if len(lines) < expected_lines:
        return None, data  

    result = []
    index = 1

    for _ in range(num_elements):
        value = lines[index + 1]
        result.append(value)
        index += 2

    consumed_lines = raw_lines[:expected_lines]
    remaining_lines = raw_lines[len(consumed_lines):]

    remaining_buffer = "\n".join(remaining_lines)

    return result, remaining_buffer