
import math
import pytest
from src import preprocessing


# Fixtures
@pytest.fixture
def numbers():
    """Provide a reusable list of numerical values."""
    return [1.0, 2.0, 3.0, 4.0]


@pytest.fixture
def mixed_values():
    """Provide a list containing different missing values."""
    return [1, None, "", "nan", 2, float("nan"), 3]


# Cleaning tests
@pytest.mark.parametrize(
    "values, expected",
    [
        ([1, None, 2, "", 3], [1, 2, 3]),
        (["hello", "", "world"], ["hello", "world"]),
        ([None, None, ""], []),
        ([1, 2, 3], [1, 2, 3]),
        (["nan", "hello", "NaN"], ["hello"]),
    ],
)
def test_remove_missing(values, expected):
    assert preprocessing.remove_missing(values) == expected


def test_remove_missing_fixture(mixed_values):
    result = preprocessing.remove_missing(mixed_values)

    assert result == [1, 2, 3]


@pytest.mark.parametrize(
    "values, fill_value, expected",
    [
        ([1, None, 2], 0, [1, 0, 2]),
        ([1, "", 2], -1, [1, -1, 2]),
        ([None, "nan"], "missing", ["missing", "missing"]),
    ],
)
def test_fill_missing(values, fill_value, expected):
    assert preprocessing.fill_missing(values, fill_value) == expected


def test_fill_missing_default(mixed_values):
    assert preprocessing.fill_missing(mixed_values) == [1, 0, 0, 0, 2, 0, 3]


def test_remove_duplicates():
    values = [1, 2, 2, 3, 1, 4]
    assert preprocessing.remove_duplicates(values) == [1, 2, 3, 4]


def test_remove_duplicates_with_strings():
    values = ["apple", "banana", "apple", "orange"]
    assert preprocessing.remove_duplicates(values) == [
        "apple", "banana", "orange"
    ]


# Numeric tests

@pytest.mark.parametrize(
    "values, new_min, new_max, expected",
    [
        ([1, 2, 3], 0, 1, [0.0, 0.5, 1.0]),
        ([1, 2, 3], -1, 1, [-1.0, 0.0, 1.0]),
        ([10, 20, 30], 0, 10, [0.0, 5.0, 10.0]),
    ],
)
def test_normalize(values, new_min, new_max, expected):
    result = preprocessing.normalize(values, new_min, new_max)

    assert result == pytest.approx(expected)


def test_normalize_fixture(numbers):
    result = preprocessing.normalize(numbers)

    assert result == pytest.approx([0.0, 1 / 3, 2 / 3, 1.0])


def test_normalize_empty_list():
    assert preprocessing.normalize([]) == []


def test_normalize_constant_values():
    assert preprocessing.normalize([5, 5, 5]) == [0.0, 0.0, 0.0]


def test_normalize_invalid_range():
    with pytest.raises(ValueError):
        preprocessing.normalize([1, 2, 3], 10, 0)


def test_standardize(numbers):
    result = preprocessing.standardize(numbers)

    assert sum(result) == pytest.approx(0.0)
    assert result == pytest.approx([
        -1.3416407865,
        -0.4472135955,
        0.4472135955,
        1.3416407865,
    ])


def test_standardize_constant_values():
    assert preprocessing.standardize([5, 5, 5]) == [0.0, 0.0, 0.0]


def test_standardize_empty_list():
    assert preprocessing.standardize([]) == []


def test_clip():
    values = [-5, 0, 5, 10, 15]

    assert preprocessing.clip(values, 0, 10) == [0, 0, 5, 10, 10]


def test_clip_invalid_range():
    with pytest.raises(ValueError):
        preprocessing.clip([1, 2, 3], 10, 0)


def test_convert_to_integers():
    values = ["10", "abc", "20", "3.5", "-5"]

    assert preprocessing.convert_to_integers(values) == [10, 20, -5]


def test_convert_to_integers_empty():
    assert preprocessing.convert_to_integers([]) == []


def test_logarithmic():
    values = [1, 2, 0, -5, 10]

    result = preprocessing.logarithmic(values)

    assert result == pytest.approx([
        math.log(1),
        math.log(2),
        math.log(10),
    ])


def test_logarithmic_empty():
    assert preprocessing.logarithmic([]) == []


# Text tests

def test_tokenize():
    text = "Hello World! Python 123."

    assert preprocessing.tokenize(text) == [
        "hello", "world", "python", "123"
    ]


def test_tokenize_empty():
    assert preprocessing.tokenize("") == []


def test_remove_punctuation():
    text = "Hello, World! Python 123."

    assert preprocessing.remove_punctuation(text) == "Hello World Python 123"


def test_remove_punctuation_empty():
    assert preprocessing.remove_punctuation("") == ""


def test_remove_stopwords():
    text = "The cat is sitting on the table"
    stopwords = ["the", "is", "on"]

    assert preprocessing.remove_stopwords(text, stopwords) == "cat sitting table"


def test_remove_stopwords_case_insensitive():
    text = "THE CAT IS HERE"
    stopwords = ["the", "is"]

    assert preprocessing.remove_stopwords(text, stopwords) == "cat here"


# Structure tests

def test_flatten():
    values = [[1, 2], [3, 4], [5, 6]]

    assert preprocessing.flatten(values) == [1, 2, 3, 4, 5, 6]


def test_flatten_empty():
    assert preprocessing.flatten([]) == []


def test_shuffle():
    values = [1, 2, 3, 4, 5]

    result = preprocessing.shuffle(values, seed=42)

    assert sorted(result) == sorted(values)


def test_shuffle_reproducibility():
    values = [1, 2, 3, 4, 5]

    first = preprocessing.shuffle(values, seed=42)
    second = preprocessing.shuffle(values, seed=42)

    assert first == second


def test_shuffle_does_not_modify_original():
    values = [1, 2, 3, 4, 5]

    preprocessing.shuffle(values, seed=42)

    assert values == [1, 2, 3, 4, 5]
