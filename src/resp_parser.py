def parse_resp(data: str):

    ##Normalize line endings
    data = data.replace("\r\n", "\n")

    lines = data.split("\n")

    ##To Remove empty lines
    lines = [line for line in lines if line.strip() != ""]

    if not lines:
        return []

    ##fallback
    if not lines[0].startswith("*"):
        return [data.strip()]

    try:
        num_elements = int(lines[0][1:])
    except:
        return []

    result = []
    index = 1

    for _ in range(num_elements):
        if index + 1 >= len(lines):
            break

        value = lines[index + 1]
        result.append(value)

        index += 2

    return result