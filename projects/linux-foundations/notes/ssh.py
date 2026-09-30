"""
Notes on using SSH.

This module contains plain‑text documentation that complements the programmatic
helpers in :pymod:`projects.linux_foundations.ssh`.  It is deliberately kept
simple and does not import any heavy dependencies; the content is intended to
be read by developers learning how to work with SSH from the command line and
from Python.

Typical topics covered:

* Generating a key pair with ``ssh-keygen``.
* Adding the public key to ``~/.ssh/authorized_keys`` on the remote host.
* Testing connectivity with ``ssh -o BatchMode=yes``.
* Running remote commands via ``ssh``.
* Copying files with ``scp`` or ``rsync``.
* Common pitfalls (host key verification, permissions, agent forwarding).

The notes are provided as a string constant so that they can be displayed
programmatically, for example::

    from projects.linux_foundations.notes.ssh import SSH_NOTES
    print(SSH_NOTES)

"""

SSH_NOTES = """
SSH (Secure Shell) is the de‑facto standard for encrypted remote login and
command execution.  Below is a quick cheat‑sheet for everyday use.

1. **Generate a key pair**

   ```sh
   ssh-keygen -t rsa -b 4096 -C "your@email.com" -f ~/.ssh/id_rsa_mykey
   ```

   * ``-t`` selects the key type (rsa, ed25519, …).
   * ``-b`` sets the key size for RSA keys.
   * ``-C`` adds a comment (often an email address).
   * ``-f`` specifies the output file.

2. **Copy the public key to the remote host**

   ```sh
   ssh-copy-id -i ~/.ssh/id_rsa_mykey.pub user@remote.example.com
   ```

   Alternatively, append the contents of ``id_rsa_mykey.pub`` to
   ``~/.ssh/authorized_keys`` on the remote side.

3. **Test the connection (no password prompt)**

   ```sh
   ssh -o BatchMode=yes -o StrictHostKeyChecking=no user@remote.example.com echo ok
   ```

   The ``BatchMode`` option disables interactive password prompts, which is
   useful for scripts.  ``StrictHostKeyChecking=no`` avoids the “host key
   verification” prompt on first use – use with care.

4. **Run a remote command**

   ```sh
   ssh user@remote.example.com "ls -l /var/www"
   ```

   Quoting is important: the whole remote command must be a single argument
   to the local ``ssh`` binary.

5. **Copy files**

   * Using ``scp`` (simple, works everywhere):

     ```sh
     scp -P 2222 local.txt user@remote.example.com:/tmp/
     ```

   * Using ``rsync`` (efficient for large or incremental transfers):

     ```sh
     rsync -avz -e "ssh -p 2222" local_dir/ user@remote.example.com:/remote/dir/
     ```

6. **Common pitfalls**

   * **Permissions** – ``~/.ssh`` should be ``700`` and the private key
     ``600``; otherwise the SSH client will refuse to use the key.
   * **Host key verification** – the first time you connect, SSH asks to
     confirm the host’s fingerprint.  In automated scripts you can set
     ``StrictHostKeyChecking=no`` or manage known hosts manually.
   * **Agent forwarding** – if you need to use your local keys on a remote
     host, enable it with ``ssh -A`` and ensure ``ForwardAgent yes`` in your
     ``~/.ssh/config``.

7. **Python helpers**

   The :pymod:`projects.l