# libkosciuszko

kosciuszko is a simple vault for storing secrets on GNU/Linux. It is heavily inspired by [encnote](https://git.sr.ht/~shakna/encnote).

This lib implements all basic features. See also [kosciuszko-utils](https://git.sr.ht/~happy_shredder/kosciuszko-utils) for CLI interfaces.

# Rationale

All existing approaches to storing arbitrary secrets on Linux are shit. kosciuszko is a general purpose vault which supercedes all existing approaches. It uses standard technologies and so can easily be implemented in e.g. shell or any arbitrary language.

## Method
Unsecured secrets are stored in a directory. This directory is then folded into a squashfs, and then encrypted with a GPG key.
To access secrets, the process is simply reversed.

# Usage

Import with `python3 -m pip install --user libkosciuszko`. Create a kosciuszko object with

```{.python}
gpg_id = "example@example.com"	# Email, key name, key ID etc
store = "example.kos"			# Filename
kosciuszko = Kosciuszko(gpg_id, store)
```

There are several core methods.

```{.python}
kosciuszko.new() 					# Initialise a new store
ls = kosciuszko.list() 				# List contents of a store, either in machine friendly or user-friendly formats (detailed=True flag)
kosciuszko.addfile(filename, data) 	# Add a file called filename, containing data `data` (bytes)
kosciuszko.getfile(filename) 		# Retrieve file called filename
```
