# iBooks highlights export

Export your iBooks highlights and notes to markdown files.  Modified from [original][] by [shrsv][].

[original]: https://github.com/shrsv/ibooks_highlights_export
[shrsv]:    https://github.com/shrsv

## What it does

The scripts reads the local sqlite database that iBooks uses to track annotations.  It proceeds to generate a markdown file corresponding to each book in the database, and populate it with the associated highlights and notes.

It preserves each book's identifier (and some other data) in the YAML header of the markdown file. You can actually rename the file and the next run of the script will find and update the appropriate file.  Additionally, it creates a **My notes** section for additional free-form notes that it won't overwrite on subsequent updates.

## Usage

Simplest way to get your highlights:

```
$ python setup.py install
$ ibooks-highlights.py sync
$ ll books
```

What you get per book:

```
---
asset_id: 3AB4BC5DE2CAAEE41EBF569B5CD1B70F
author: REISNER MARC
modified_date: '2017-09-02T14:18:36'
title: Cadillac Desert
---

# Cadillac Desert

By REISNER MARC

## My notes <a name="my_notes_dont_delete"></a>



## iBooks notes <a name="ibooks_notes_dont_delete"></a>

### Introduction

Westerners call what they have established out here a civilization, but it would
be more accurate to call it a beachhead. And if history is any guide, the odds
that we can sustain it would have to be regarded as low.

Everything depends on the manipulation of water—on capturing it behind dams,
storing it, and rerouting it in concrete rivers over distances of hundreds of
miles. Were it not for a century and a half of messianic effort toward that end,
the West as we know it would not exist.
```

## Options

To get a list of books (asterisk means there's unsynced highlights):

```
$ ibooks-highlights.py list

D36605A6   1	Bayesian Methods for Hackers
80EE27E1   27	Dune
E5875B57 * 30	Making of the Atomic Bomb
7029A581   17	Meditations - Modern Library Translation
547526C9   50	Musashi
F6C97901   77	The Idea Factory
```

To set output directory:

```
$ ibooks-highlights.py -b other-books sync
```

Change default output directory via environment variable:

```
export IBOOKS_HIGHLIGHT_DIRECTORY=some/other/folder
```

## TODO

- [ ] `¯\_(ツ)_/¯`
