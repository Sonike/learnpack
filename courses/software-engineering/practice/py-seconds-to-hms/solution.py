def seconds_to_hms(seconds: int) -> str:
    """Turn a number of seconds into "HH:MM:SS"."""
    hours = seconds // 3600
    rest = seconds % 3600
    minutes = rest // 60
    secs = rest % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


if __name__ == "__main__":
    print(seconds_to_hms(3723))   # 01:02:03
    print(seconds_to_hms(59))     # 00:00:59
