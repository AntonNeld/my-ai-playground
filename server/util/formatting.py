import math


def format_prefix(value, unit):
    magnitudes = [
        ("n", 1e-9),
        ("μ", 1e-6),
        ("m", 1e-3),
        ("", 1),
        ("k", 1e3),
        ("M", 1e6),
        ("G", 1e9),
        ("T", 1e12)
    ]

    for prefix, factor in magnitudes:
        # We're not rounding properly here, but it's not
        # important to get it exactly right
        normalized_value = math.floor(value/factor)
        if normalized_value < 1000 or prefix == magnitudes[-1][0]:
            return f"{normalized_value} {prefix}{unit}"
