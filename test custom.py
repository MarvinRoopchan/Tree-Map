from typing import List
from tree_data import coordinate_leaf
import os
import pytest

from tree_data import coordinates_in_range, AbstractTree, FileSystemTree

RECT = (0, 0, 1024, 738)

RECR = (0, 0, 738, 1024)


def test1() -> None:
    assert coordinates_in_range((0, 0, 204, 738), (114, 409)) is True


def test2() -> None:

    assert coordinates_in_range((0, 0, 204, 738), (443, 512)) is False


def test3() -> None:

    assert coordinates_in_range((0, 0, 204, 738), (784, 334)) is False


def test4() -> None:

    assert coordinates_in_range((204, 0, 512, 738), (114, 409)) is False


def test5() -> None:
    assert coordinates_in_range((204, 0, 512, 738), (443, 512)) is True


def test6() -> None:

    assert coordinates_in_range((204, 0, 512, 738), (784, 334)) is False


def test7() -> None:

    assert coordinates_in_range((716, 0, 308, 738), (114, 409)) is False


def test8() -> None:

    assert coordinates_in_range((716, 0, 308, 738), (443, 512)) is False


def test9() -> None:

    assert coordinates_in_range((716, 0, 308, 738), (784, 334)) is True



def test_tree1() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/test_tree_map')

    data = file.generate_treemap((0, 0, 1024, 738))

    raw = [((0, 0, 165, 738), (202, 40, 234)), ((165, 0, 412, 738), (58, 18, 181)), ((577, 0, 447, 410), (189, 53, 115)), ((577, 410, 447, 328), (245, 130, 184))]

    for i in range(len(data)):
        assert data[i][0] == raw[i][0]


def test_tree_2() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/test_2')

    data = file.generate_treemap((0, 0, 1024, 738))

    raw = [((0, 0, 1024, 738), (42, 163, 10))]

    for i in range(len(data)):
        assert data[i][0] == raw[i][0]


def test_tree3() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/test_3')

    data = file.generate_treemap((0, 0, 1024, 738))

    raw = [(0, 0, 1, 738), (1, 0, 236, 738), (237, 0, 787, 738)]

    for i in range(len(data)):

        assert data[i][0] == raw[i]


def test_handout() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/example_handout')

    data = file.generate_treemap((0, 0, 200, 100))

    raw = [((0, 0, 40, 100), (17, 201, 110)), ((40, 0, 100, 100), (146, 227, 103)), ((140, 0, 60, 100), (68, 81, 87))]

    for i in range(len(data)):
        assert data[i][0] == raw[i][0]


def test_advanced() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/advanced_example')

    data = file.generate_treemap((0, 0, 1024, 738))

    raw = [(0, 0, 130, 214), (130, 0, 251, 214), (0, 214, 381, 360), (0, 574, 381, 164), (381, 0, 193, 735), (381, 735, 193, 3), (574, 0, 91, 738), (665, 0, 225, 738), (890, 0, 134, 738)]

    for i in range(len(data)):
        assert data[i][0] == raw[i]


def test_folder() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/all_folder_example')

    data = file.generate_treemap((0, 0, 1024, 738))

    raw = [(0, 0, 491, 738), (491, 0, 399, 738), (890, 0, 134, 738)]

    for i in range(len(data)):
        assert data[i][0] == raw[i]


def test_blank() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/blank')

    data = file.generate_treemap((0, 0, 1024, 738))

    assert data == []


def test_folder_with_file() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/folders_and files')

    data = file.generate_treemap((0, 0, 1024, 738))

    result = [(0, 0, 128, 738), (128, 0, 429, 738), (557, 0, 348, 738), (905, 0, 119, 738)]

    for i in range(len(data)):
        assert data[i][0] == result[i]


def test_file_last() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/100bytes')

    data = file.generate_treemap((0, 0, 1024, 738))

    raw = [(0, 0, 543, 738), (543, 0, 100, 738), (643, 0, 77, 738), (720, 0, 54, 738), (774, 0, 250, 738)]

    for i in range(len(data)):
        assert data[i][0] == raw[i]


def test_trouble() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/trouble')

    date = file.generate_treemap((0, 0, 1024, 738))

    raw = [(0, 0, 193, 738), (193, 0, 302, 738), (495, 0, 529, 426), (495, 426, 529, 312)]

    for i in range(len(date)):

        assert date[i][0] == raw[i]


def test_init_blank() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/blank')

    assert file._parent_tree is None

    assert len(file._subtrees) == 1

    for i in range(3):
        assert file.colour[i] >= 0
        assert file.colour[i] <= 255

    assert file.data_size == 0

    assert file._subtrees[0].data_size == 0

    assert file._root == 'blank'

    assert file._subtrees[0]._root == 'New folder'


def test_init_f_a_f() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/folders_and files')

    assert file.data_size == 595869

    assert file._parent_tree is None

    for i in range(3):
        assert file.colour[i] >= 0
        assert file.colour[i] <= 255

    count = 0
    for sub in file._subtrees:
        count += sub.data_size
        assert sub._parent_tree is file
        for i in range(3):
            assert file.colour[i] >= 0
            assert file.colour[i] <= 255

    assert count == file.data_size

    subtrees = os.listdir('C:/Users/Marvin/Downloads/folders_and files')
    subs = []

    for sub in file._subtrees:
        subs.append(sub._root)

    assert subtrees == subs


def test_init__100bytes() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/100bytes')

    assert file.data_size == 132

    assert file._parent_tree is None

    _parent_tree_checker(file, file._subtrees)

    for i in range(3):
        assert file.colour[i] >= 0
        assert file.colour[i] <= 255

    count = 0
    for sub in file._subtrees:
        count += sub.data_size
        assert sub._parent_tree is file
        for i in range(3):
            assert file.colour[i] >= 0
            assert file.colour[i] <= 255

    assert count == file.data_size

    subtrees = os.listdir('C:/Users/Marvin/Downloads/100bytes')
    subs = []

    for sub in file._subtrees:
        subs.append(sub._root)

    assert subtrees == subs


def test_init_advanced() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/advanced_example')

    assert file.data_size == 40090

    assert file._parent_tree is None

    _parent_tree_checker(file, file._subtrees)

    for i in range(3):
        assert file.colour[i] >= 0
        assert file.colour[i] <= 255

    count = 0
    for sub in file._subtrees:
        count += sub.data_size
        assert sub._parent_tree is file
        for i in range(3):
            assert file.colour[i] >= 0
            assert file.colour[i] <= 255

    assert count == file.data_size

    subtrees = os.listdir('C:/Users/Marvin/Downloads/advanced_example')
    subs = []

    for sub in file._subtrees:
        subs.append(sub._root)

    assert subtrees == subs


def test_init_Windir() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/WinDirStatPortable')

    assert file.data_size == 2132529

    assert file._parent_tree is None

    _parent_tree_checker(file, file._subtrees)

    for i in range(3):
        assert file.colour[i] >= 0
        assert file.colour[i] <= 255

    count = 0
    for sub in file._subtrees:
        count += sub.data_size
        assert sub._parent_tree is file
        for i in range(3):
            assert file.colour[i] >= 0
            assert file.colour[i] <= 255

    assert count == file.data_size

    subtrees = os.listdir('C:/Users/Marvin/Downloads/WinDirStatPortable')
    subs = []

    for sub in file._subtrees:
        subs.append(sub._root)

    assert subtrees == subs


def test_init_assignments() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads/assignments')

    assert file.data_size == 32179465

    assert file._parent_tree is None

    _parent_tree_checker(file, file._subtrees)

    for i in range(3):
        assert file.colour[i] >= 0
        assert file.colour[i] <= 255

    count = 0
    for sub in file._subtrees:
        count += sub.data_size
        assert sub._parent_tree is file
        for i in range(3):
            assert file.colour[i] >= 0
            assert file.colour[i] <= 255

    assert count == file.data_size

    subtrees = os.listdir('C:/Users/Marvin/Downloads/assignments')
    subs = []

    for sub in file._subtrees:
        subs.append(sub._root)

    assert subtrees == subs


def test_init_big_download() -> None:

    file = FileSystemTree('C:/Users/Marvin/Downloads')

    assert file._parent_tree is None

    _parent_tree_checker(file, file._subtrees)

    for i in range(3):
        assert file.colour[i] >= 0
        assert file.colour[i] <= 255

    count = 0
    for sub in file._subtrees:
        count += sub.data_size
        assert sub._parent_tree is file
        for i in range(3):
            assert file.colour[i] >= 0
            assert file.colour[i] <= 255

    assert count == file.data_size

    subtrees = os.listdir('C:/Users/Marvin/Downloads')
    subs = []

    for sub in file._subtrees:
        subs.append(sub._root)

    assert subtrees == subs


def test_right_click() -> None:

    blank = FileSystemTree('C:/Users/Marvin/Downloads/blank')

    dic = coordinate_leaf(blank.leaves(), blank.generate_treemap((RECT)))

    for x in range(RECT[2] + 1):
        for y in range(RECT[3] + 1):
            blank.mouse_right((x, y), RECT)

    assert len(blank) == 2
    assert blank.data_size == 0


def _parent_tree_checker(main: AbstractTree, tree: List[AbstractTree]) -> None:
    """ checks if the parent tree of each subtree is the node above it.

    returns True iff above condition is met False otherwise.
    """
    for subtree in tree:
        assert subtree._parent_tree == main
        assert True is isinstance(subtree, AbstractTree)

    for subtree in tree:
        _parent_tree_checker(subtree, subtree._subtrees)


if __name__ == '__main__':
    pytest.main(['test custom.py'])
