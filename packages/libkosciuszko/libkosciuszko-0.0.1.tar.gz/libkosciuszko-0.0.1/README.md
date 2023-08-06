# libkosciuszko

kosciuszko is a simple vault for storing secrets on GNU/Linux. It is heavily inspired by [encnote](https://git.sr.ht/~shakna/encnote).

# Rationale

All existing approaches to storing arbitrary secrets on Linux are shit.

Unsecured secrets are stored in a directory. This directory is then folded into a squashfs, and then encrypted with a GPG key.
To access secrets, the process is simply reversed.

# Usage

dunno
