import ast

import pytest
from click.testing import CliRunner

from src.cli import cli


# Fixture
@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


# Clean commands
def test_remove_missing(runner):
    result = runner.invoke(
        cli, ["clean", "remove-missing", "10,,20,nan,30"]
    )

    assert result.exit_code == 0
    assert result.output.strip() == "['10', '20', '30']"


def test_fill_missing(runner):
    result = runner.invoke(
        cli, ["clean", "fill-missing", "10,,20"]
    )

    assert result.exit_code == 0
    assert result.output.strip() == "['10', '0', '20']"


def test_fill_missing_custom_value(runner):
    result = runner.invoke(
        cli, ["clean", "fill-missing", "10,,20", "--fill-value", "missing"]
    )

    assert result.exit_code == 0
    assert result.output.strip() == "['10', 'missing', '20']"


# Numeric commands

def test_normalize(runner):
    result = runner.invoke(
        cli, ["numeric", "normalize", "10,20,30"]
    )

    assert result.exit_code == 0
    assert ast.literal_eval(result.output) == [0.0, 0.5, 1.0]


def test_normalize_custom_range(runner):
    result = runner.invoke(
        cli, ["numeric", "normalize", "10,20,30", "--min", "-1", "--max", "1"]
    )

    assert result.exit_code == 0
    assert ast.literal_eval(result.output) == [-1.0, 0.0, 1.0]


def test_standardize(runner):
    result = runner.invoke(
        cli, ["numeric", "standardize", "1,2,3"]
    )

    assert result.exit_code == 0

    values = ast.literal_eval(result.output)

    assert sum(values) == pytest.approx(0.0)


def test_clip(runner):
    result = runner.invoke(
        cli,
        ["numeric","clip", "--min", "0", "--max", "10", "--", "-5,5,15"],
    )

    assert result.exit_code == 0
    assert ast.literal_eval(result.output) == [0.0, 5.0, 10.0]


def test_convert_to_integers(runner):
    result = runner.invoke(
        cli, ["numeric", "convert-to-integers", "10,abc,20,30"]
    )

    assert result.exit_code == 0
    assert ast.literal_eval(result.output) == [10, 20, 30]


def test_logarithmic(runner):
    result = runner.invoke(
        cli, ["numeric", "logarithmic", "1,2,10"]
    )

    assert result.exit_code == 0

    values = ast.literal_eval(result.output)

    assert values == pytest.approx([0.0, 0.69314718056, 2.30258509299])


# Text commands

def test_tokenize(runner):
    result = runner.invoke(
        cli, ["text", "tokenize", "Hello World 123!"]
    )

    assert result.exit_code == 0
    assert ast.literal_eval(result.output) == [
        "hello", "world", "123"
    ]


def test_remove_punctuation(runner):
    result = runner.invoke(
        cli, ["text", "remove-punctuation", "Hello, World!"]
    )

    assert result.exit_code == 0
    assert result.output.strip() == "Hello World"


def test_remove_stopwords(runner):
    result = runner.invoke(
        cli,
        [
            "text",
            "remove-stopwords",
            "the cat is here",
            "--stopword", "the",
            "--stopword", "is",
        ],
    )

    assert result.exit_code == 0
    assert result.output.strip() == "cat here"


# Structure commands

def test_shuffle(runner):
    result = runner.invoke(
        cli, ["struct", "shuffle", "1,2,3,4,5", "--seed", "42"]
    )

    assert result.exit_code == 0

    values = ast.literal_eval(result.output)

    assert sorted(values) == ["1", "2", "3", "4", "5"]


def test_flatten(runner):
    result = runner.invoke(
        cli, ["struct", "flatten", "[[1,2],[3,4],[5]]"]
    )

    assert result.exit_code == 0
    assert ast.literal_eval(result.output) == [1, 2, 3, 4, 5]


def test_unique(runner):
    result = runner.invoke(
        cli, ["struct", "unique", "10,20,10,30,20"]
    )

    assert result.exit_code == 0
    assert ast.literal_eval(result.output) == ["10", "20", "30"]


# General CLI tests

def test_cli_help(runner):
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "clean" in result.output
    assert "numeric" in result.output
    assert "text" in result.output
    assert "struct" in result.output
