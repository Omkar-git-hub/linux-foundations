"""
Utility functions for basic text processing tasks.

This module provides a small collection of pure‑Python helpers that are
useful when working with plain text strings.  The functions are deliberately
kept simple and have no external dependencies – they rely only on the
standard library.

Typical usage::

    from projects.linux_foundations.text_processing import (
        word_count,
        unique_words,
        most_common_word,
        reverse_words,
        char_frequency,
    )

    text = "Hello world! Hello again."
    print(word_count(text))          # -> 4
    print(unique_words(text))        # -> {'hello', 'world', 'again'}
    print(most_common_word(text))    # -> 'hello'
    print(reverse_words(text))       # -> "again. Hello world! Hello"
    print(char_frequency(text))      # -> {'H': 2, 'e': 4, ...}
"""

from __future__ import annotations

import collections
import re
from typing import Counter, Dict, Iterable, List, Set, Tuple

__all__: Tuple[str, ...] = (
    "normalize_text",
    "tokenize",
    "word_count",
    "unique_words",
    "most_common_word",
    "reverse_words",
    "char_frequency",
)


def normalize_text(text: str) -> str:
    """
    Return a lower‑cased version of *text* with punctuation stripped.

    The function removes characters that are not alphanumeric or whitespace.
    This makes subsequent tokenisation case‑insensitive and punctuation‑free.

    Parameters
    ----------
    text:
        The raw input string.

    Returns
    -------
    str
        Normalised text.
    """
    # Keep letters, numbers and whitespace; replace everything else with a space.
    cleaned = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return cleaned.lower()


def tokenize(text: str) -> List[str]:
    """
    Split *text* into a list of words.

    The implementation first normalises the text (lower‑case, punctuation
    removal) and then splits on any whitespace sequence.

    Parameters
    ----------
    text:
        Input string.

    Returns
    -------
    list[str]
        List of word tokens; empty list if *text* contains no words.
    """
    normalized = normalize_text(text)
    # ``split`` without arguments treats consecutive whitespace as a single separator.
    return normalized.split()


def word_count(text: str) -> int:
    """
    Count the number of words in *text*.

    Words are defined by the :func:`tokenize` function.

    Parameters
    ----------
    text:
        Input string.

    Returns
    -------
    int
        Number of words.
    """
    return len(tokenize(text))


def unique_words(text: str) -> Set[str]:
    """
    Return the set of distinct words appearing in *text*.

    The comparison is case‑insensitive and ignores punctuation.

    Parameters
    ----------
    text:
        Input string.

    Returns
    -------
    set[str]
        Unique words.
    """
    return set(tokenize(text))


def most_common_word(text: str) -> str | None:
    """
    Determine the most frequently occurring word in *text*.

    If the input contains no words, ``None`` is returned.  In the case of a
    tie, the word that appears first in alphabetical order is chosen
    (the behaviour of :class:`collections.Counter.most_common`).

    Parameters
    ----------
    text:
        Input string.

    Returns
    -------
    str | None
        The most common word, or ``None`` when *text* is empty.
    """
    tokens = tokenize(text)
    if not tokens:
        return None
    counter: Counter[str] = collections.Counter(tokens)
    most_common, _ = counter.most_common(1)[0]
    return most_common


def reverse_words(text: str) -> str:
    """
    Return a new string with the order of words reversed.

    The original whitespace and punctuation are not preserved; the output
    consists of the words (as defined by :func:`tokenize`) joined by a single
    space.

    Parameters
    ----------
    text:
        Input string.

    Returns
    -------
    str
        Words in reverse order.
    """
    tokens = tokenize(text)
    return " ".join(reversed(tokens))


def char_frequency(text: str) -> Dict[str, int]:
    """
    Compute the frequency of each character in *text*.

    The function treats the string as a raw sequence of Unicode code points;
    it does **not** perform any normalisation.

    Parameters
    ----------
    text:
        Input string.

    Returns
    -------
    dict[str, int]
        Mapping from character to its occurrence count.
    """
    return dict(collections.Counter(text))