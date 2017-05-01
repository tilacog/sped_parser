from sped_parser.nodes import SpedNode


def test_length_flat():
    node = SpedNode(None, [])
    assert len(node) == 1


def test_length_depth_one():
    # this node have 3 children with zero children each
    node = SpedNode(None, [
        SpedNode(None, []),
        SpedNode(None, []),
        SpedNode(None, []),
    ])

    assert len(node) == 4  # 1 + 3


def test_length_depth_two():
    # this node has child that has two children.
    node = SpedNode(None, [
        SpedNode(None, [
            SpedNode(None, []),
            SpedNode(None, []),
        ])
    ])

    assert len(node) == 4


# test iter_tree
# --------------
def test_iter_tree_single_structure():
    node = SpedNode(None, [])
    assert list(node) == [node]


def test_iter_tree_simple_nested_structure():
    child = SpedNode(None, [])
    parent = SpedNode(None, [child])

    assert list(parent) == [parent, child]


def test_iter_tree_complex_nested_structure():
    child = SpedNode(None, [])
    parent = SpedNode(None, [child])
    uncle = SpedNode(None, [])
    root = SpedNode(None, [parent, uncle])

    assert list(root) == [root, parent, child, uncle]


# test filter_tree
# ----------------
def test_filter_tree_simple_case():
    node = SpedNode(None, [
        SpedNode('foo', []),
        SpedNode('bar', [])
    ])

    node.filter(lambda n: n.content != 'foo')

    expected = SpedNode(None, [SpedNode('bar', [])])
    assert node == expected


def test_filter_tree_complex_case():
    child = SpedNode('child', [])
    parent = SpedNode(None, [child])
    uncle = SpedNode(None, [])
    root = SpedNode(None, [parent, uncle])

    root.filter(lambda n: n.content != 'child')

    assert list(root) == [root, parent, uncle]
