def parse_resp(data: str):

    data = data.replace("\r\n", "\n")
    lines = data.split("\n")

    # Remove empty lines at start
    while lines and lines[0].strip() == "":
        lines.pop(0)

    if not lines:
        return None, data

    # Non-RESP fallback
    if not lines[0].startswith("*"):
        return [lines[0].strip()], "\n".join(lines[1:])

    try:
        num_elements = int(lines[0][1:])
    except:
        return None, data

    expected_lines = 1 + num_elements * 2

    if len(lines) < expected_lines:
        return None, data  # not complete yet

    result = []
    index = 1

    for _ in range(num_elements):
        value = lines[index + 1]
        result.append(value)
        index += 2

    remaining = "\n".join(lines[expected_lines:])

    return result, remaining