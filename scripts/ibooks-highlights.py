#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import click

from ibooks_highlights.models import BookList
from ibooks_highlights import ibooksdb


def get_booklist(path: pathlib.Path) -> BookList:

    book_list = BookList(path)
    annos = ibooksdb.fetch_annotations()
    book_list.populate_annotations(annos)
    return book_list


@click.group()
@click.option('--bookdir', '-b', type=click.Path(), 
              envvar='IBOOKS_HIGHLIGHT_DIRECTORY', default='./books')
@click.pass_context
def cli(ctx, bookdir):

    # create directory if it doesn't exist
    p = pathlib.Path(bookdir)
    p.mkdir(parents=True, exist_ok=True)

    ctx.obj['BOOKDIR'] = p


@cli.command()
@click.pass_context
def list(ctx):

    bookdir = ctx.obj['BOOKDIR']
    bl = get_booklist(bookdir)

    books = [b for b in bl.books.values()]
    books = sorted(books, key=lambda b: b.title)
    for book in books:
        print(book)


@cli.command()
@click.option('--force', '-f', is_flag=True)
@click.option('--file_type', '-ftype',
              type=click.Choice(['org', 'md']), default='org')
@click.pass_context
def sync(ctx, force, file_type):

    bookdir = ctx.obj['BOOKDIR']
    bl = get_booklist(bookdir)

    bl.write_modified(bookdir, force, file_type)


if __name__ == '__main__':
    cli(obj={})
