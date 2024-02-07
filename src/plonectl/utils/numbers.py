def format_bytes(size: int) -> str:
    """Format bytes and add suffix."""
    power = 2**10
    n = 0
    power_labels = {0: "b", 1: "Kb", 2: "Mb", 3: "Gb", 4: "Tb"}
    while size >= power:
        size /= power
        n += 1
    label = power_labels[n]
    return f"{size:.2f}{label}" if n > 0 else f"{size}{label}"


def format_int(size: int) -> str:
    """Format integer with thousand separator."""
    return f"{size:,}"
