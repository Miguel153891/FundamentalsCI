"""Functions for cleaning and preprocessing data."""

import math
import random
import re
from typing import Any


# Cleaning functions
def _is_missing(value: Any) -> bool:
    """Check if a value is missing (if it's None, '', nan, etc.)"""
    if value is None:
        return True

    if isinstance(value, str) and value.strip().lower() in ("", "nan"):
        return True

    if isinstance(value, (int, float)) and math.isnan(value):
        return True

    return False


def remove_missing(values: list[Any]) -> list[Any]:
    """Remove missing values from a list."""
    result = []

    for value in values:
        if not _is_missing(value):
            result.append(value)

    return result


def fill_missing(values: list[Any], fill_value: Any = 0) -> list[Any]:
    """Replace missing values with a specified value."""
    result = []

    for value in values:
        if _is_missing(value):
            result.append(fill_value)
        else:
            result.append(value)

    return result


def remove_duplicates(values: list[Any]) -> list[Any]:
    """Remove duplicated values while preserving order."""
    result = []

    for value in values:
        if value not in result:
            result.append(value)

    return result


# Numeric functions


def normalize(
    values: list[float], new_min: float = 0.0, new_max: float = 1.0
) -> list[float]:
    """Normalize values using min-max scaling."""
    if not values:
        return []

    if new_min > new_max:
        raise ValueError("new_min cannot exceed new_max")

    old_min = min(values)
    old_max = max(values)

    if (
        old_min == old_max
    ):  # If oldmin and max are equal, the list is the same value repeated
        return [new_min] * len(values)

    result = []

    for value in values:
        normalized = new_min + (
            (value - old_min) * (new_max - new_min) / (old_max - old_min)
        )
        result.append(normalized)

    return result


def standardize(values: list[float]) -> list[float]:
    """Standardize values using z-score."""
    if not values:
        return []

    mean = sum(values) / len(values)

    variance = sum((value - mean) ** 2 for value in values) / len(values)

    std_dev = math.sqrt(variance)

    if std_dev == 0:
        return [0.0] * len(values)

    result = []

    for value in values:
        result.append((value - mean) / std_dev)

    return result


def clip(values: list[float], minimum: float, maximum: float) -> list[float]:
    """Clip values to a specified range."""
    if minimum > maximum:
        raise ValueError("minimum cannot exceed maximum")

    result = []

    for value in values:
        if value < minimum:
            result.append(minimum)
        elif value > maximum:
            result.append(maximum)
        else:
            result.append(value)

    return result


def convert_to_integers(values: list[str]) -> list[int]:
    """Convert valid values to integers."""
    result = []

    for value in values:
        try:
            result.append(int(value))
        except (ValueError, TypeError):
            continue

    return result


def logarithmic(values: list[float]) -> list[float]:
    """Apply natural logarithm to positive values."""
    result = []

    for value in values:
        if value > 0:
            result.append(math.log(value))

    return result


# Text functions


def tokenize(text: str) -> list[str]:
    """Extract lowercase alphanumeric words."""
    return re.findall(r"[^\W_]+", text.lower())


def remove_punctuation(text: str) -> str:
    """Keep only alphanumeric characters and spaces."""
    result = ""

    for character in text:
        if character.isalnum() or character.isspace():
            result += character

    return result


def remove_stopwords(text: str, stopwords: list[str]) -> str:
    """Remove stopwords from lowercase text."""
    words = text.lower().split()
    stopwords = [word.lower() for word in stopwords]

    result = []

    for word in words:
        if word not in stopwords:
            result.append(word)

    return " ".join(result)


# Structure functions


def flatten(values: list[list[Any]]) -> list[Any]:
    """Flatten a list of lists."""
    result = []

    for sublist in values:
        for item in sublist:
            result.append(item)

    return result


def shuffle(values: list[Any], seed: int | None = None) -> list[Any]:
    """Return a shuffled copy of a list."""
    result = values.copy()
    random.Random(seed).shuffle(result)

    return result
