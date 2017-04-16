from itertools import takewhile
from typing import List, NamedTuple

from record_relations import relations


# Data model
# ----------
SpedNode = NamedTuple('SpedNode', [('content', str), ('children', List)])


def values(node):
    "returns a SpedNode values as a list"
    return node.content.split('|')


def record_type(node):
    "returns the record type of a SpedNode"
    return values(node)[0]


def as_text(node):
    "renders a SpedNode as a sped-like file"
    text = ('|' + '|'.join(values(node)) + '|\n') if node.content else ''
    text += ''.join(as_text(c) for c in node.children)
    return text


# Parser utilities
# ----------------
def update_tracker(tracker, node):
    "tracks the last known node for a given record type."
    rec_type = record_type(node)
    tracker[rec_type] = node
    return tracker


def strip_line(text):
    "custom function for stripping characters out of sped lines"
    return text.strip()[1:-1]


def sped_iterator(sped_file_handle):
    "simple iterator for sped files"
    def predicate(text):
        try:
            return text[4] == '|'
        except KeyError:
            return False
    return takewhile(predicate, (strip_line(i) for i in sped_file_handle))


def build_tree(sped_file_path, specification_file_path):
    """reads a sped file and a specification file and returns a SpedNode
    tree.
    """
    nodes = []
    tracker = {}
    record_relations = relations(specification_file_path)

    with open(sped_file_path, encoding='latin-1') as f:
        for line in sped_iterator(f):
            node = SpedNode(line, [])
            tracker = update_tracker(tracker, node)

            parent_record_type = record_relations[record_type(node)]

            parent = tracker.get(parent_record_type)
            if parent:
                parent.children.append(node)
            else:
                nodes.append(node)

    # return root node
    return SpedNode(content=None, children=nodes)


# Iteration
# ---------
def iter_tree(node):
    "depth-first traverseal of a tree"
    yield node
    for child in node.children:
        yield child
        for sub_child in child.children:
            yield from iter_tree(sub_child)


def length(node):
    "count nodes inside"
    if not node.children:
        return 1
    return 1 + sum(length(c) for c in node.children)


if __name__ == '__main__':
    import sys
    SAMPLE_FILE_PATH = sys.argv[1]
    SPECIFICATION_FILE = 'efd_contribuicoes-0-4008-1.json'

    tree = build_tree(SAMPLE_FILE_PATH, SPECIFICATION_FILE)

    print(as_text(tree))
