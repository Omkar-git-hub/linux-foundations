"""
Bash scripting notes and helper utilities.

This module provides small helper functions that return example Bash
scripts as strings.  The functions are deliberately simple – they are
intended for educational purposes and unit‑testing of string handling
logic rather than for executing the scripts directly.

Typical usage
-------------
>>> from projects.linux-foundations.notes.bash_scripting import (
...     get_hello_world_script,
...     get_for_loop_script,
... )
>>> print(get_hello_world_script())
#!/usr/bin/env bash
echo "Hello, World!"
"""

from __future__ import annotations

__all__ = [
    "get_hello_world_script",
    "get_for_loop_script",
    "get_if_else_script",
]


def get_hello_world_script() -> str:
    """
    Return a minimal “Hello, World!” Bash script.

    The script uses ``#!/usr/bin/env bash`` as the shebang for maximum
    portability across Unix‑like systems.

    Returns
    -------
    str
        The script source code.
    """
    return """#!/usr/bin/env bash
echo "Hello, World!"
"""


def get_for_loop_script(iterable_name: str = "items") -> str:
    """
    Return a Bash ``for`` loop script that iterates over a space‑separated
    list stored in a variable.

    Parameters
    ----------
    iterable_name : str, optional
        The name of the variable that holds the items to iterate over.
        Defaults to ``"items"``.

    Returns
    -------
    str
        The script source code.
    """
    return f"""#!/usr/bin/env bash
{iterable_name}="one two three"
for element in ${{{iterable_name}}}; do
    echo "Element: ${{element}}"
done
"""


def get_if_else_script(condition: str = '[ "$var" -eq 1 ]') -> str:
    """
    Return a Bash script that demonstrates an ``if``/``else`` construct.

    Parameters
    ----------
    condition : str, optional
        The test condition to evaluate.  The default checks whether the
        variable ``var`` equals ``1`` using the ``[ ... ]`` test command.

    Returns
    -------
    str
        The script source code.
    """
    return f"""#!/usr/bin/env bash
var=1
if {condition}; then
    echo "Condition is true."
else
    echo "Condition is false."
fi
"""