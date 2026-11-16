def seconds_to_hms(seconds: int) -> str:
    """Turn a number of seconds into "HH:MM:SS"."""
    # TODO: hours = seconds // 3600, and the rest = seconds % 3600
    # TODO: split the rest into minutes and seconds the same way, with 60
    # TODO: format each part with :02d
    return "00:00:00"


if __name__ == "__main__":
    print(seconds_to_hms(3723))   # 01:02:03
    print(seconds_to_hms(59))     # 00:00:59
