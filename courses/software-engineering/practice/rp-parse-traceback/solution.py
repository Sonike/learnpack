def parse_traceback(text: str) -> dict:
    """Return {"type", "message", "file", "line"} for the innermost frame of a traceback."""
    lines = text.strip().splitlines()

    # The last line is "ExceptionType: message", or just "ExceptionType".
    exc_type, _, message = lines[-1].partition(": ")

    # The innermost frame is the last 'File "...", line N, in ...' line.
    frame = ""
    for line in lines:
        if line.strip().startswith('File "'):
            frame = line.strip()

    file_name = frame.split('"')[1]
    line_part = frame.split(", line ")[1]
    line_number = int(line_part.split(",")[0])

    return {"type": exc_type, "message": message, "file": file_name, "line": line_number}
