from itertools import islice, takewhile
from typing import List

from .record_relations import relations


# Data model
# ----------
class SpedNode:
    def __init__(self, content, children=[], parent=None):
        self.content = content if content else ''
        self.children = children
        self.parent = parent

    @property
    def values(self):
        return self.content.split('|')

    @values.setter
    def values(self, list_of_values):
        self.content = '|'.join(list_of_values)

    @property
    def record_type(self):
        return self.values[0]

    def as_text(self):
        "renders a SpedNode as a sped-like file"
        self_content = '|' + self.content + '|\n'
        children_content = ''.join(c.as_text() for c in self.children)
        return self_content + children_content

    def find_all(self, predicate):
        "generator "
        yield from (node for node in self if predicate(node))

    def find(self, predicate):
        "returns the first occurence of node that passes the predicate test"
        iterator = islice(self.find_all(self, predicate), 1)
        return next(iterator)

    def get_node(self, record_type):
        "returns the first occurence of node for that record type"
        return self.find(self, lambda n: n.record_type == record_type)

    def filter(self, predicate):
        """recursively removes child nodes whenever `predicate(child)` returns
        true"""
        self.children = [c for c in self.children if predicate(c)]
        for c in self.children:
            c.filter(predicate)

    def __eq__(self, other):
        if not isinstance(other, SpedNode):
            return False

        if self.content != other.content:
            return False

        if self.children != other.children:
            return False
        return True

    def __len__(self):
        return 1 + sum(len(c) for c in self.children)

    def __iter__(self):
        yield self
        for child in self.children:
            yield from child

    def __repr__(self):
        len_children = sum(len(c) for c in self.children)
        return "<SpedNode(%s, %s children)>" % (repr(self.record_type),
                                                len_children)


# Parser utilities
# ----------------
def sped_iterator(sped_file_handle):
    "simple iterator for sped files"

    def strip_line(text):
        "helper function for stripping unwanted characters out of sped lines"
        return text.strip()[1:-1]

    def predicate(text):
        try:
            return text[4] == '|'
        except IndexError:
            return False
    return takewhile(predicate, (strip_line(i) for i in sped_file_handle))


def build_tree(sped_file_path, specification_file_path):
    """reads a sped file and a specification file and returns a list of nodes
    (forest).
    """
    forest = []
    tracker = {}
    record_relations = relations(specification_file_path)

    with open(sped_file_path, encoding='latin-1') as f:
        for line in sped_iterator(f):
            node = SpedNode(line, [])
            tracker[node.record_type] = node

            parent_record_type = record_relations[node.record_type]

            parent = tracker.get(parent_record_type)

            if parent:
                parent.children.append(node)
                node.parent = parent
            else:
                forest.append(node)

        return forest


# Forest functions
# ----------------
Forest = List[SpedNode]


def forest_iterator(forest: Forest):
    for node in forest:
        yield from node


def forest_find_all(forest: Forest, predicate):
    for node in forest:
        yield from node.find_all(predicate)


def forest_find(forest: Forest, predicate):
    return next(islice(forest_find_all(forest, predicate), 1))


def forest_get_node(forest: Forest, record_type):
    return forest_find(forest, lambda n: n.record_type == record_type)