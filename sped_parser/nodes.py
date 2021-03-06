from itertools import islice, takewhile
from typing import List


# Data model
# ----------
class SpedNode:

    def __init__(self, content, children=[], parent=None):
        if isinstance(content, list):
            assert content
            for el in content:
                assert isinstance(el, str)
            self.values = content
        elif isinstance(content, str):
            if not content:
                content = '.'
            else:
                content = content.strip()
                if content[0] == "|" and content[-1] == "|":
                    content = content[1:-1]
            self.values = content.split("|")

        self.children = list(children)
        for child_node in children:
            child_node.parent = self

        if parent and self not in parent.children:
                parent.insert(self)
        self.parent = parent

    @property
    def record_type(self):
        return self.values[0]

    def as_text(self):
        "renders a SpedNode as a sped-like file"
        self_content = '|' + '|'.join(self.values) + '|\n'
        children_content = ''.join(c.as_text() for c in self.children)
        return self_content + children_content

    def find_all(self, predicate):
        "return all direct "
        yield from (node for node in self if predicate(node))

    def find(self, predicate):
        "returns the first occurence of node that passes the predicate test"
        iterator = islice(self.find_all(predicate), 1)
        return next(iterator)

    def get_node(self, record_type):
        "returns the first occurence of node for that record type"
        return next(self.get_nodes(record_type))

    def get_nodes(self, record_type):
        "generates all descendant nodes that match the given record type"
        generator = self.find_all(lambda n: n.record_type == record_type)
        yield from generator

    def filter(self, predicate):
        """recursively removes child nodes whenever `predicate(child)` returns
        true"""
        self.children = [c for c in self.children if predicate(c)]
        for c in self.children:
            c.filter(predicate)

    def count(self):
        "returns number of nodes (including self)"
        return 1 + sum(c.count() for c in self.children)

    def update(self, index, new_value):
        "DEPRECATED. Use `node[index] = new_value` instead."
        self.values[index] = new_value

    def insert(self, node):
        "inserts a node into self.children in an appropriate position"

        # base case: children is an empty list
        if not self.children:
            self.children.append(node)
        else:
            pos = (idx for idx, sibling in enumerate(self.children)
                   if sibling.record_type >= node.record_type)
            try:
                index = next(pos)
            except StopIteration:
                self.children.append(node)
            else:
                # using slices because `list.insert` causes RecursionErrors
                self.children = (self.children[:index]
                                 + [node]
                                 + self.children[index:])
        node.parent = self

    def ancestors(self):
        yield self
        if self.parent:
            yield from self.parent.ancestors()

    def delete(self):
        self.parent.children.remove(self)

    def __eq__(self, other):
        if not isinstance(other, SpedNode):
            return False

        if self.values != other.values:
            return False

        if self.children != other.children:
            return False
        return True

    def __hash__(self):
        return hash(tuple(self.values))

    def __iter__(self):
        yield self
        for child in self.children:
            yield from child

    def __getitem__(self, index):
        return self.values[index]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __repr__(self):
        return "<SpedNode(%s)>" % (repr(self.record_type),)


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


def build_forest(sped_file_path, record_relations):
    """reads a sped file and a relations dictionary and returns a list of nodes
    (forest).
    """
    forest = []
    tracker = {}

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


def forest_get_nodes(forest: Forest, record_type):
    yield from forest_find_all(forest, lambda n: n.record_type == record_type)


def forest_as_text(forest: Forest):
    "serializes a forest as a sped file"
    return ''.join(node.as_text() for node in forest)


def forest_size(forest):
    "returns the count of all nodes inside a forest"
    return sum(tree.count() for tree in forest)


def forest_size_by_prefix(forest, prefix):
    "returns the count of all forest nodes for a given record_type prefix"
    return sum(tree.count() for tree in forest
               if tree.record_type.startswith(prefix))
