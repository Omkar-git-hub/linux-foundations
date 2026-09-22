"""
Notes – Text Processing

This notebook‑style module contains explanatory material that complements the
functions defined in :pymod:`projects.linux_foundations.text_processing`.

The goal is to provide a quick reference for learners who are exploring basic
string manipulation techniques in Python.

--- Overview ---------------------------------------------------------------

* **Normalization** – Converting text to a canonical form (lower‑casing,
  stripping punctuation) makes many analyses easier and more reliable.

* **Tokenisation** – Splitting a string into atomic units (words) is the
  foundation for counting, searching and many natural‑language‑processing
  tasks.

* **Counting & Frequency** – ``collections.Counter`` is a handy tool for
  building histograms of words or characters.

* **Reversing** – Re‑ordering words can be useful for exercises or for
  generating simple transformations.

--- Example ---------------------------------------------------------------

>>> from projects.linux_foundations.text_processing import (
...     word_count, unique_words, most_common_word,
...     reverse_words, char_frequency,
... )
>>> sample = "Hello, world! Hello again."
>>> word_count(sample)
4
>>> unique_words(sample)
{'hello', 'world', 'again'}
>>> most_common_word(sample)
'hello'
>>> reverse_words(sample)
'again hello world hello'
>>> char_frequency(sample)['l']
5

--- Further Reading ---------------------------------------------------------

* The official Python documentation for :pymod:`re` – regular expressions.
* :pymod:`collections` – especially :class:`collections.Counter`.
* Unicode handling in Python – ``str`` objects are Unicode by default.

Feel free to experiment with the functions in an interactive session or
extend them for more sophisticated processing (e.g., stemming, stop‑word
removal, n‑gram generation).
"""

# The notes module does not expose any runtime symbols; it exists solely for
# documentation purposes.  Keeping an explicit ``__all__`` makes the intent
# clear to static analysis tools.

__all__: list[str] = []