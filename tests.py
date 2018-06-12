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


def test_iter_wont_raise_recursion_error():
    "this test setup used to raise a RecursiveErrror due to list.insert method"
    parent = SpedNode('parent')
    son = SpedNode('son', children=[SpedNode('grandchild')])

    assert parent.count() == 1
    assert son.count() == 2

    parent.insert(son)

    assert parent.count() == 3


def test_parent_iteration():
    child = SpedNode('child', [])
    parent = SpedNode('parent', [])
    parent.insert(child)
    assert child.parent is parent
    assert list(child.ancestors()) == [child, parent]

    # test another insertion method
    child2 = SpedNode('child2', [])
    parent2 = SpedNode('parent2', [child2])
    assert child2.parent is parent2
    assert list(child2.ancestors()) == [child2, parent2]

    # yet another insertion method
    parent3 = SpedNode('parent3', [])
    child3 = SpedNode('child3', [], parent=parent3)
    assert child3.parent is parent3
    assert list(child3.ancestors()) == [child3, parent3]


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

# test get_nodes
# --------------
def test_get_node():
    children = [
        SpedNode('foo'),
        SpedNode('bar'),
        SpedNode('baz'),
    ]
    parent = SpedNode(None, children)

    result = parent.get_node('bar')
    assert result == SpedNode('bar')

def test_get_nodes():
    children = [
        SpedNode('foo'),
        SpedNode('bar'),
        SpedNode('baz'),
        SpedNode('bar'),
    ]
    parent = SpedNode(None, children)

    result = list(parent.get_nodes('bar'))
    assert result == [SpedNode('bar')] * 2


# test insert
# -----------
def test_insert_order_pre():
    children = [SpedNode('b'), SpedNode('c')]
    parent = SpedNode(None, children=children)
    parent.insert(SpedNode('a'))
    assert parent.children == [
        SpedNode('a'), SpedNode('b'), SpedNode('c')
    ]


def test_insert_order_mid():
    children = [SpedNode('a'), SpedNode('c')]
    parent = SpedNode(None, children=children)
    parent.insert(SpedNode('b'))
    assert parent.children == [
        SpedNode('a'), SpedNode('b'), SpedNode('c')
    ]


def test_insert_order_pos():
    children = [SpedNode('a'), SpedNode('b')]
    parent = SpedNode(None, children=children)
    parent.insert(SpedNode('c'))
    assert parent.children == [
        SpedNode('a'), SpedNode('b'), SpedNode('c')
    ]

def test_insert_order_mixed_pre():
    children = [SpedNode('b'), SpedNode('b')]
    parent = SpedNode(None, children=children)
    parent.insert(SpedNode('a'))
    assert parent.children == [
        SpedNode('a'), SpedNode('b'), SpedNode('b')
    ]


def test_insert_order_mixed_pos():
    children = [SpedNode('a'), SpedNode('a')]
    parent = SpedNode(None, children=children)
    parent.insert(SpedNode('b'))
    assert parent.children == [
        SpedNode('a'), SpedNode('a'), SpedNode('b')
    ]
