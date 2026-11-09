
import math
import random
import re
from typing import Any



# Cleaning functions

def remove_missing(values: list[Any]) -> list[Any]:
    """Remove None, empty strings and NaN values."""
    result = []

    for value in values:
        is_missing = (
            value is None
            or (isinstance(value, str) and value.strip().lower() in ("", "nan"))
            or (
                isinstance(value, (int, float))
                and math.isnan(value)
            )
        )

        if not is_missing:
            result.append(value)

    return result


def fill_missing(
    values: list[Any], fill_value: Any = 0
) -> list[Any]:
    """Replace missing values with a specified value."""
    return [
        fill_value if value is None
        or (isinstance(value, str) and value.strip().lower() in ("", "nan"))
        or (
            isinstance(value, (int, float))
            and math.isnan(value)
        )
        else value
        for value in values
    ]


def remove_duplicates(values: list[Any]) -> list[Any]:
    """Remove duplicated values while preserving order."""
    return list(dict.fromkeys(values))


# Numeric functions

def normalize(
    values: list[float],
    new_min: float = 0.0,
    new_max: float = 1.0,
) -> list[float]:
    """Normalize numerical values using min-max scaling."""
    if not values:
        return []

    if new_min > new_max:
        raise ValueError("new_min cannot exceed new_max")

    old_min = min(values)
    old_max = max(values)

    if old_min == old_max:
        return [new_min for _ in values]

    return [
        new_min + (value - old_min) * (new_max - new_min)
        / (old_max - old_min)
        for value in values
    ]


def standardize(values: list[float]) -> list[float]:
    """Standardize numerical values using z-score."""
    if not values:
        return []

    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        return [0.0 for _ in values]

    return [(value - mean) / std_dev for value in values]


def clip(
    values: list[float],
    minimum: float,
    maximum: float,
) -> list[float]:
    """Clip numerical values to a specified range."""
    if minimum > maximum:
        raise ValueError("minimum cannot exceed maximum")

    return [
        max(minimum, min(value, maximum))
        for value in values
    ]


def convert_to_integers(values: list[str]) -> list[int]:
    """Convert valid strings to integers, ignoring invalid values."""
    result = []

    for value in values:
        try:
            result.append(int(value))
        except (ValueError, TypeError):
            continue

    return result


def logarithmic(values: list[float]) -> list[float]:
    """Apply natural logarithm to positive values only."""
    return [math.log(value) for value in values if value > 0]


# Text functions


def tokenize(text: str) -> list[str]:
    """Extract lowercase alphanumeric words from text."""
    return re.findall(r"[^\W_]+", text.lower())


def remove_punctuation(text: str) -> str:
    """Keep only alphanumeric characters and spaces."""
    return "".join(
        character for character in text
        if character.isalnum() or character.isspace()
    )


def remove_stopwords(text: str, stopwords: list[str]) -> str:
    """Remove stopwords from lowercase text."""
    words = text.lower().split()
    stopwords = [word.lower() for word in stopwords]

    return " ".join(
        word for word in words if word not in stopwords
    )


# Structure functions

def flatten(values: list[list[Any]]) -> list[Any]:
    """Flatten a list of lists into a single list."""
    return [
        item
        for sublist in values
        for item in sublist
    ]


def shuffle(values: list[Any], seed: int | None = None) -> list[Any]:
    """Return a shuffled copy of a list."""
    result = values.copy()
    random.Random(seed).shuffle(result)
    return result
