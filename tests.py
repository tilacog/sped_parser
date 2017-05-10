from sped_parser.nodes import SpedNode


def test_length_flat():
    node = SpedNode(None, [])
    assert node.count() == 1


def test_length_depth_one():
    # this node have 3 children with zero children each
    node = SpedNode(None, [
        SpedNode(None, []),
        SpedNode(None, []),
        SpedNode(None, []),
    ])

    assert node.count() == 4  # 1 + 3


def test_length_depth_two():
    # this node has child that has two children.
    node = SpedNode(None, [
        SpedNode(None, [
            SpedNode(None, []),
            SpedNode(None, []),
        ])
    ])

    assert node.count() == 4


# test iteration
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


# test filter
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


# test getitem
# ------------
def test_getitem():
    node = SpedNode('foo|bar|baz')
    assert node[0] == 'foo'
    assert node[1] == 'bar'
    assert node[2] == 'baz'


# test update
# -----------
def test_update():
    node = SpedNode('foo|bar|baz')
    node.update(2, 'qux')
    assert node.values == ['foo', 'bar', 'qux']


def test_update_with_slice():
    node = SpedNode('foo|bar|baz')
    node.update(slice(0, 2), ['hey', 'joe'])
    assert node.values == ['hey', 'joe', 'baz']
