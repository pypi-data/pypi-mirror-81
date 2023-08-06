# kosciuszko-utils

kosciuszko is a simple vault for storing secrets on GNU/Linux. It is heavily inspired by [encnote](https://git.sr.ht/~shakna/encnote).

These utils implement a basic CLI for using a store. See also [libkosciuszko](https://git.sr.ht/~happy_shredder/libkosciuszko) for the core lib.

# Rationale

All existing approaches to storing arbitrary secrets on Linux are shit. kosciuszko is a general purpose vault which supercedes all existing approaches. It uses standard technologies and so can easily be implemented in e.g. shell or any arbitrary language.

## Method
Unsecured secrets are stored in a directory. This directory is then folded into a squashfs, and then encrypted with a GPG key.
To access secrets, the process is simply reversed.

# Usage

`python3 -m pip --user install kosciuszko-utils`

This provides the bins `kosciuszko-new`, `kosciuszko-addfile`, `kosciuszko-list`, `kosciuszko-extract-file`, `kosciuszko-extract`. 
Which should all be self explanatory. Like git, these may be invoked like `kosciuszko new ...` and so on.

This is alpha quality software; there may be bugs.

# Homepage

<https://git.sr.ht/~happy_shredder/kosciuszko-utils>

# License

GPLv3+
