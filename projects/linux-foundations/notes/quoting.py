"""
Quoting Notes
=============

This module documents the quoting mechanisms available in POSIX‑compatible
shells.  Understanding quoting is essential for writing robust command
lines and scripts because it determines how the shell interprets special
characters, whitespace, and variable expansions.

Quoting Types
-------------

1. **Single Quotes (`'...'`)**
   - Preserve the literal value of each character within the quotes.
   - No expansion (parameter, command, arithmetic, pathname) occurs.
   - To embed a single quote, close the existing quotes, escape the quote,
     and reopen: ``'It'"'"'s a test'`` → ``It's a test``.

2. **Double Quotes (`"..."`)**
   - Preserve most characters literally but allow:
     * Parameter expansion: ``"$VAR"``
     * Command substitution: ``"$(cmd)"``
     * Arithmetic expansion: ``"$((expr))"``
     * Escape sequences with backslash for ``$``, ``"``, ``\``, and newline.
   - Useful for strings that contain spaces yet need variable expansion.

3. **ANSI‑C Quoting (`$'...'`)** – Bash‑specific
   - Interprets backslash‑escaped characters (e.g., ``\n``, ``\t``) similar to C strings.
   - Example: ``$'Line1\nLine2'`` produces a two‑line output.

4. **Backslash Escaping (`\`)**
   - Escapes the following character, preventing its special meaning.
   - Outside quotes, ``\`` can escape spaces, tabs, newlines, and metacharacters.
   - Inside double quotes, ``\`` only escapes ``$``, ``"``, ``\``, and newline.

5. **Here‑Document (`<<`) and Here‑String (`<<<`)**
   - The delimiter can be quoted to control expansion:
     * ``<<'EOF'`` – no expansion inside the document.
     * ``<<"EOF"`` – variable and command substitution occur.

Practical Tips
--------------

* Prefer single quotes when the string contains no variables; this avoids
  accidental expansion and is the most performant.
* Use double quotes for strings that need variable or command substitution.
* When mixing quotes, close the current quote, insert the needed literal,
  and reopen a new quote rather than trying to escape inside single quotes.
* Remember that ``$'...'`` is not POSIX‑standard; scripts intended for
  portability should avoid it.

Common Pitfalls
---------------

* Forgetting to quote variables: ``rm $file`` will split on whitespace,
  while ``rm "$file"`` treats the entire value as a single argument.
* Nested quoting errors: ``echo "He said, 'Hello'"`` works, but
  ``echo 'He said, "Hello"'`` is also valid; mixing the wrong type can
  lead to syntax errors.
* Unintended globbing: ``echo "$var"*`` expands the asterisk after the
  variable expansion, potentially matching files.

Further Reading
----------------

* Bash Reference Manual – *Quoting*.
* POSIX.1‑2017 – *Shell Command Language* – Section on quoting.
"""

# Documentation‑only module; no runtime code required.
pass