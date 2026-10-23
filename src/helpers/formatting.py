def format_duration(ms: int) -> str:
    minutes, seconds = divmod(int(ms / 1000), 60)
    return f"{minutes}:{seconds:02d}"
