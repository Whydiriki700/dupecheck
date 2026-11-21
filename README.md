# dupecheck

Your disk is full and you do not know why. dupecheck finds the duplicate
files, by content, not by name, and tells you exactly how much space the
extra copies waste.

The same photo saved under three names is one file to dupecheck. Files are
grouped by size first, then compared by sha256 content hash, so different
files that merely share a name or a size are never accused.

## Usage

```
python -m dupecheck ~/Pictures ~/Downloads
python -m dupecheck ~/Pictures --min-size 1000000 --plan
python -m dupecheck ~/Pictures --json
```

`--plan` marks the first file of each group as KEEP and the rest as COPY,
so you can review a cleanup before doing it.

## Safety

dupecheck never deletes, moves, or renames anything. It only reads and
reports. What you do with the copies is your call.

## Example output

```
scanned: 4211 files; duplicate groups: 37; wasted: 812.4 MB

812.0 KB each, 3 copies, wasted 1.6 MB
  foto-liburan.jpg
  foto-liburan (1).jpg
  backup/foto-liburan.jpg
```

## Tests

```
python -m unittest discover -s tests
```

Zero dependencies. Python 3.9+. MIT license.
