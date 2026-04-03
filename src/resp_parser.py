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
        return ["ERROR"], ""

    expected_lines = 1 + num_elements * 2

    if len(lines) < expected_lines:
        return None, data

    result = []
    index = 1

    try:
        for _ in range(num_elements):
            if not lines[index].startswith("$"):
                return ["ERROR"], ""

            value = lines[index + 1]
            result.append(value)
            index += 2
    except:
        return ["ERROR"], ""

    remaining = "\n".join(lines[expected_lines:])

    return result, remaining