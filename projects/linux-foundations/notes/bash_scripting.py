"""
Bash Scripting Notes

This module contains a concise collection of Bash scripting concepts,
best‑practice tips, and frequently used patterns. The notes are provided
as a plain‑text string that can be imported and displayed by other parts
of the ``linux‑foundations`` package or by external tools.

Typical usage:

    from projects.linux_foundations.notes.bash_scripting import get_notes

    print(get_notes())
"""

# The core notes are stored in a module‑level constant. Keeping the data
# separate from the accessor function makes it easy to reuse the string
# directly (e.g. for documentation generation) while still offering a
# convenient API.

NOTES: str = """\
# Bash Scripting Cheat Sheet

## Shebang & Script Execution
- Start scripts with a shebang to define the interpreter:
  ```bash
  #!/usr/bin/env bash
  ```
- Make the script executable:
  ```bash
  chmod +x script.sh
  ```
- Run with `./script.sh` or `bash script.sh`.

## Variables
- Assign without spaces: `var="value"`
- Access with `$var` or `${var}`.
- Read‑only: `readonly VAR="value"`
- Export to child processes: `export VAR`

## Parameter Expansion
- Default values:
  ```bash
  ${var:-default}   # use default if var is unset or empty
  ${var:=default}   # assign default if var is unset or empty
  ${var:+alt}       # use alt if var is set and non‑empty
  ```
- Substring: `${var:offset:length}`
- Length: `${#var}`
- Replace:
  ```bash
  ${var/pattern/repl}   # first match
  ${var//pattern/repl}  # all matches
  ```

## Arrays
```bash
arr=(one two three)
echo "${arr[0]}"      # first element
echo "${arr[@]}"      # all elements
len=${#arr[@]}        # number of elements
```

## Conditional Expressions
```bash
if [[ $var == pattern ]]; then
    # ...
elif (( $num > 10 )); then
    # ...
fi
```
- Use `[[ ... ]]` for string/regex tests, `(( ... ))` for arithmetic.

## Loops
```bash
# For loop over list
for item in "${arr[@]}"; do
    echo "$item"
done

# C‑style loop
for ((i=0; i<10; i++)); do
    echo $i
done

# While loop
while [[ -n $input ]]; do
    read -r input
done
```

## Functions
```bash
my_func() {
    local arg1="$1"
    echo "Argument: $arg1"
}
my_func "test"
```
- Use `local` to avoid polluting the global namespace.

## Error Handling
- Exit on error: `set -e` (or `set -o errexit`).
- Treat unset variables as errors: `set -u`.
- Enable pipefail: `set -o pipefail`.
- Combine: `set -euo pipefail`.

## Debugging
- Enable tracing: `set -x` (or run script with `bash -x script.sh`).
- Use `printf` for formatted output instead of `echo`.

## Input/Output
- Read a line: `read -r var`
- Read into array: `read -ra arr <<< "$string"`
- Redirect stdout: `command > file.txt`
- Append: `command >> file.txt`
- Redirect stderr: `command 2> err.txt`
- Combine: `command > out.txt 2>&1`

## Here Documents & Here Strings
```bash
cat <<EOF
Multi‑line text
EOF

grep "pattern" <<< "$string"
```

## Process Substitution
```bash
diff <(sort file1) <(sort file2)
```

## Common One‑liners
- Find and delete empty files:
  `find . -type f -empty -delete`
- Count lines, words, bytes:
  `wc -lwm file`
- Show top 10 memory‑hogs:
  `ps aux --sort=-%mem | head -n 10`

## Miscellaneous Tips
- Quote variables: always use `"$var"` unless you deliberately need word splitting.
- Prefer `$(command)` over backticks `` `command` ``.
- Use `printf` for portable output (handles escape sequences reliably).
- When looping over `find` results, use `while IFS= read -r` to handle spaces/newlines.
"""

def get_notes() -> str:
    """
    Return the Bash scripting notes as a plain‑text string.

    Returns
    -------
    str
        The multi‑line Bash scripting cheat sheet.
    """
    return NOTES

__all__ = ["NOTES", "get_notes"]