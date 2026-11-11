"""Command-line interface for the data preprocessing project."""

import json

import click

from . import preprocessing


# Helper functions
def parse_list(values):
    """Convert comma-separated values into a list."""
    return values.split(",")


def parse_numbers(values):
    """Convert comma-separated values into floats."""
    return [float(value) for value in values.split(",")]


# Main CLI group
@click.group()
def cli():
    """Data preprocessing command-line interface."""


# Clean commands
@cli.group()  # Clean group is c
def clean():
    """Commands for cleaning data."""


@clean.command()
@click.argument("values")
def remove_missing(values):
    """Remove missing values from a list.

    Example: cli clean remove-missing "10,,20,nan,30"
    """
    values = parse_list(values)
    result = preprocessing.remove_missing(values)
    click.echo(result)


@clean.command()
@click.argument("values")
@click.option(
    "--fill-value",
    default=0,
    type=str,
    help="Value used to replace missing values. Default: 0.",
)
def fill_missing(values, fill_value):
    """Replace missing values with a specified value.

    Example: cli clean fill-missing "10,,20" --fill-value 0
    """
    values = parse_list(values)
    result = preprocessing.fill_missing(values, fill_value)
    click.echo(result)


# Numeric commands


@cli.group()
def numeric():
    """Commands for processing numerical data."""


@numeric.command()
@click.argument("values")
@click.option(
    "--min", "new_min", default=0.0, type=float, help="Minimum value of the new range."
)
@click.option(
    "--max", "new_max", default=1.0, type=float, help="Maximum value of the new range."
)
def normalize(values, new_min, new_max):
    """Normalize values using min-max scaling.

    Example: cli numeric normalize "10,20,30" --min 0 --max 1
    """
    values = parse_numbers(values)
    result = preprocessing.normalize(values, new_min, new_max)
    click.echo(result)


@numeric.command()
@click.argument("values")
def standardize(values):
    """Standardize values using z-score.

    Example: cli numeric standardize "10,20,30"
    """
    values = parse_numbers(values)
    result = preprocessing.standardize(values)
    click.echo(result)


@numeric.command()
@click.argument("values")
@click.option(
    "--min", "minimum", default=0.0, type=float, help="Minimum value allowed."
)
@click.option(
    "--max", "maximum", default=1.0, type=float, help="Maximum value allowed."
)
def clip(values, minimum, maximum):
    """Clip values to a specified range.

    Example: cli numeric clip "0.5,2,5" --min 0 --max 1
    """
    values = parse_numbers(values)
    result = preprocessing.clip(values, minimum, maximum)
    click.echo(result)


@numeric.command()
@click.argument("values")
def convert_to_integers(values):
    """Convert valid strings into integers.

    Example: cli numeric convert-to-integers "10,abc,20,30"
    """
    values = parse_list(values)
    result = preprocessing.convert_to_integers(values)
    click.echo(result)


@numeric.command()
@click.argument("values")
def logarithmic(values):
    """Apply logarithmic transformation to positive values.

    Example: cli numeric logarithmic "1,2,10,100"
    """
    values = parse_numbers(values)
    result = preprocessing.logarithmic(values)
    click.echo(result)


# Text commands


@cli.group()
def text():
    """Commands for processing textual data."""


@text.command()
@click.argument("input_text")
def tokenize(input_text):
    """Split text into lowercase alphanumeric words.

    Example: cli text tokenize "Hello World 123!"
    """
    result = preprocessing.tokenize(input_text)
    click.echo(result)


@text.command()
@click.argument("input_text")
def remove_punctuation(input_text):
    """Remove punctuation and special characters from text.

    Example: cli text remove-punctuation "Hello, World!"
    """
    result = preprocessing.remove_punctuation(input_text)
    click.echo(result)


@text.command()
@click.argument("input_text")
@click.option(
    "--stopword",
    multiple=True,
    help="Stopword to remove. Can be specified multiple times.",
)
def remove_stopwords(input_text, stopword):
    """Remove specified stopwords from text.

    Example: cli text remove-stopwords "the cat is here" --stopword the --stopword is
    """
    result = preprocessing.remove_stopwords(input_text, list(stopword))
    click.echo(result)


# Structure commands


@cli.group()
def struct():
    """Commands for manipulating data structures."""

@struct.command()
@click.argument("values")
@click.option(
    "--seed", default=None, type=int, help="Integer seed for reproducible shuffling."
)
def shuffle(values, seed):
    """Shuffle a list of values.

    Example: cli struct shuffle "10,20,30,40" --seed 42
    """
    values = parse_list(values)
    result = preprocessing.shuffle(values, seed)
    click.echo(result)


@struct.command()
@click.argument("values")
def flatten(values):
    """Flatten a list of lists.

    Example: cli struct flatten "[[1,2],[3,4],[5]]"
    """
    values = json.loads(values)
    result = preprocessing.flatten(values)
    click.echo(result)


@struct.command()
@click.argument("values")
def unique(values):
    """Remove duplicated values while preserving order.

    Example: cli struct unique "10,20,10,30,20"
    """
    values = parse_list(values)
    result = preprocessing.remove_duplicates(values)
    click.echo(result)


if __name__ == "__main__":
    cli()
