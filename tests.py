from nodes import SpedNode, length, iter_tree

# test length
# -----------

def test_length_flat():
    node = SpedNode(None, [])
    assert length(node) == 1


def test_length_depth_one():
    # this node have 3 children with zero children each
    node = SpedNode(None, [
        SpedNode(None, []),
        SpedNode(None, []),
        SpedNode(None, []),
    ])

    assert length(node) == 4  # 1 + 3


def test_length_depth_two():
    # this node has child that has two children.
    node = SpedNode(None, [
        SpedNode(None, [
            SpedNode(None, []),
            SpedNode(None, []),
        ])
    ])

    assert length(node) == 4


# test iter_tree
# --------------
def test_iter_tree_single_structure():
    node = SpedNode(None, [])
    assert list(iter_tree(node)) == [node]


def test_iter_tree_simple_nested_structure():
    child = SpedNode(None, [])
    parent = SpedNode(None, [child])

    assert list(iter_tree(parent)) == [parent, child]

def test_iter_tree_complex_nested_structure():
    child = SpedNode(None, [])
    parent = SpedNode(None, [child])
    uncle= SpedNode(None, [])
    root = SpedNode(None, [parent, uncle])

    assert list(iter_tree(root)) == [root, parent, child, uncle]
