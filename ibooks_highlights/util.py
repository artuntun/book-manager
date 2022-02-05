import re
import pathlib

from typing import (List, Dict, Optional, Union, Any, Callable)
from jinja2 import Environment, FileSystemLoader
from treelib import Tree, Node

NS_TIME_INTERVAL_SINCE_1970 = 978307200


PATH = pathlib.Path(__file__).resolve().parent / 'templates'
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(str(PATH)),
    trim_blocks=True,
    lstrip_blocks=False
)

class AnkiDirectoryError(Exception):
    pass


def render_org_tree(tree: Tree, node: Node, payload='') -> str:
    parent = tree.parent(node.identifier)
    if parent and parent.identifier.lower() == 'vocabulary':
        payload += render_vocabulary_word(tree, node)
    else:
        depth = tree.depth(node) + 1
        payload += ('*'*depth + ' ' + node.tag + '\n')
    for child in tree.children(node.identifier):
        payload += render_org_tree(tree, tree[child.identifier])
    return payload


def render_vocabulary_word(tree: Tree, node: Node) -> str:
    assert tree.parent(node.identifier)
    assert tree.parent(node.identifier).identifier.lower() == 'vocabulary'
    assert node.data
    depth = tree.depth(node) + 1
    word = node.tag
    text = ('*'*depth + ' ' + word + 2*'\n')
    if 'audio' in node.data and node.data['audio']:
        text += render_link(node.data['audio'], 'play') + '\n'
    if 'book_examples' in node.data:
        for example in node.data['book_examples']:
            text += render_quote(example)
        text += '\n'
    if 'definitions' in node.data:
        text += 'Definitions\n'
        for i, definition in enumerate(node.data['definitions']):
            text += str(i + 1) + '. ' + definition['definition']
            if 'synonyms' in definition:
                text += ' /'
                for n, synonym in enumerate(definition['synonyms']):
                    text += synonym + ', '
                    if n == 2:
                        break
                text = text[: -2]
                text += '/'
            text += '\n'
        text += '\n'
    return text


def render_quote(text: str) -> str:
    quote = '#+begin_quote' + '\n'
    quote += '#+end_quote' + '\n'
    return quote


def render_link(link: str, link_text: str = '') -> str:
    rendered_link = '[[' + link + ']'
    if link_text:
        rendered_link += '[' + link_text + ']]'
    else:
        rendered_link += ']'
    return rendered_link


def parse_epubcfi(raw: str) -> List[int]:

    if raw is None:
        return []

    parts = raw[8:-1].split(',')
    cfistart = parts[0] + parts[1]

    parts = cfistart.split(':')

    path = parts[0]
    offsets = [
        int(x[1:])
        for x in re.findall('(/\d+)', path)
    ]

    if len(parts) > 1:
        offsets.append(int(parts[1]))

    return offsets


def epubcfi_compare(x: List[int], y: List[int]) -> int:
    depth = min(len(x), len(y))
    for d in range(depth):
        if x[d] == y[d]:
            continue
        else:
            return x[d] - y[d]

    return len(x) - len(y)


def query_compare_no_asset_id(x: Dict[str, str], y: Dict[str, str]) -> int:
    return epubcfi_compare(
        parse_epubcfi(x['location']),
        parse_epubcfi(y['location'])
    )


def cmp_to_key(mycmp: Callable) -> Any:
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj: Any, *args: Any) -> None:
            self.obj = obj

        def __lt__(self, other: Any) -> Any:
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other: Any) -> Any:
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other: Any) -> Any:
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other: Any) -> Any:
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other: Any) -> Any:
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other: Any) -> Any:
            return mycmp(self.obj, other.obj) != 0
    return K
