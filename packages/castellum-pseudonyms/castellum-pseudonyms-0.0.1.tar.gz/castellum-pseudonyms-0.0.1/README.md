# Castellum Pseudonyms

Algorithms to generate, validate, and normalize pseudonyms.

This is part of the [castellum
project](https://www.mpib-berlin.mpg.de/research-data/castellum).

## Installation

    pip install castellum-pseudonyms

## Usage

    from castellum_pseudonyms import generate, clean

    # generate a new random pseudonym
    pseudonym = generate(bits=40)

    # normalize and validate a pseudonym entered by a user
    try:
        pseudonym = clean(user_input)
    except ValueError:
        print('invalid pseudonym')
