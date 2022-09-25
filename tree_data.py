"""Assignment 2: Trees for Treemap

=== CSC148 Fall 2020 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""

from __future__ import annotations
import os
from random import randint
import math

from typing import Tuple, List, Optional, Dict, Any


class AbstractTree:
    """A tree that is compatible with the treemap visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you adding and implementing
    new public *methods* for this interface.

    === Public Attributes ===
    data_size: the total size of all leaves of this tree.
    colour: The RGB colour value of the root of this tree.
        Note: only the colours of leaves will influence what the user sees.

    === Private Attributes ===
    _root: the root value of this tree, or None if this tree is empty.
    _subtrees: the subtrees of this tree.
    _parent_tree: the parent tree of this tree; i.e., the tree that contains
        this tree
        as a subtree, or None if this tree is not part of a larger tree.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - colour's elements are in the range 0-255.

    - If _root is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - _subtrees IS allowed to contain empty subtrees (this makes deletion
      a bit easier).

    - if _parent_tree is not empty, then self is in _parent_tree._subtrees
    """
    data_size: int
    colour: (int, int, int)
    _root: Optional[object]
    _subtrees: List[AbstractTree]
    _parent_tree: Optional[AbstractTree]

    def __init__(self: AbstractTree, root: Optional[object],
                 subtrees: List[AbstractTree], data_size: int = 0) -> None:
        """Initialize a new AbstractTree.

        If <subtrees> is empty, <data_size> is used to initialize this tree's
        data_size. Otherwise, the <data_size> parameter is ignored, and this
        tree's data_size is computed from the data_sizes of the subtrees.

        If <subtrees> is not empty, <data_size> should not be specified.

        This method sets the _parent_tree attribute for each subtree to self.

        A random colour is chosen for this tree.

        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees
        self._parent_tree = None

        if not subtrees:
            if self.is_empty():
                self.data_size = 0
            else:
                self.data_size = data_size
        else:
            count = 0
            for subtree in self._subtrees:
                if subtree is not None:
                    count += subtree.data_size
            self.data_size = count

        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))

        for subtree in self._subtrees:
            if subtree is not None:
                subtree._parent_tree = self

        # 1. Initialize self.colour and self.data_size,
        # according to the docstring.
        # 2. Properly set all _parent_tree attributes in self._subtrees

    def is_empty(self: AbstractTree) -> bool:
        """Return True if this tree is empty."""
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        """
        if self.is_empty():
            return 0

        size = 1  # count the root
        for subtree in self._subtrees:
            size += subtree.__len__()  # could also do len(subtree) here
        return size

    def generate_treemap(self: AbstractTree, rect: Tuple[int, int, int, int]) \
            -> List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """Run the treemap algorithm on this tree and return the rectangles.

        Each returned tuple contains a pygame rectangle and a colour:
        ((x, y, width, height), (r, g, b)).

        One tuple should be returned per non-empty leaf in this tree.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]
        """
        # Read the handout carefully to help get started identifying base cases,
        # and the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # coordinates of a rectangle, as follows.
        # x, y, width, height = rect

        if self.is_empty() or self.data_size == 0:
            return []

        if self._subtrees == [] and self._parent_tree is None:
            return [(rect, self.colour)]

        if not self._subtrees:
            if rect[2] > rect[3]:  # just a single file

                return self.base_case_width_greater(rect)

            return self.base_case_height_greater(rect)

        all_rectangles = []

        for i in range(len(self._subtrees)):

            if self._subtrees[i]._subtrees != [] and rect[2] > rect[3]:
                all_rectangles.extend(self.helper_subtree_width_greater(i, rect)
                                      )

            elif self._subtrees[i]._subtrees != [] and rect[3] >= rect[2]:

                all_rectangles.extend(self.helper_subtree_height_greater(i, rect
                                                                         ))

            elif i == len(self._subtrees) - 1 and rect[2] > rect[3]:
                final_width = self.find_last(True, rect)
                x = self.get_ith_last(True, rect, i)
                r = x, rect[1], final_width, rect[3]
                all_rectangles.extend(self._subtrees[i].generate_treemap(r))

            elif i == len(self._subtrees) - 1 and rect[3] >= rect[2]:
                final_height = self.find_last(False, rect)
                a, c = rect[0], rect[2]
                y = self.get_ith_last(False, rect, i)
                r = a, y, c, final_height
                all_rectangles.extend(self._subtrees[i].generate_treemap(r))

            elif rect[2] > rect[3]:  # HERE BUG

                all_rectangles.extend(self.file_width_greater(i, rect))

            elif rect[3] >= rect[2]:

                all_rectangles.extend(self.file_height_greater(i, rect))

        return all_rectangles

    def file_height_greater(self, i: int, rect: Tuple[int, int, int,
                                                      int]) \
            -> List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """ Helper for generate tree map when the height is greater than width

        and self has no subtrees, returns a tuple with a rectangle(s) and
        colour(s)
        """
        if i == 0:
            return self._subtrees[i].generate_treemap(rect)

        y = self.get_ith_last(False, rect, i)
        return self._subtrees[i].generate_treemap((rect[0], y, rect[2],
                                                   rect[3]))

    def file_width_greater(self, i: int, rect: Tuple[int, int, int,
                                                     int]) \
            -> List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """ Helper for generate tree map when the width is greater that height

        and self has no subtrees, returns a tuple with a rectangle(s) and
        colour(s)
        """
        if i == 0:
            return self._subtrees[i].generate_treemap(rect)

        x = self.get_ith_last(True, rect, i)
        r = x, rect[1], rect[2], rect[3]
        return self._subtrees[i].generate_treemap(r)

    def helper_subtree_width_greater(self, i: int, rect: Tuple[int, int, int,
                                                               int]) \
            -> List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """ Helper for generate tree map when the width is greater that height

        and self has subtrees, returns a tuple with a rectangle(s) and colour(s)
        """
        if i == len(self._subtrees) - 1:
            final_width = self.find_last(True, rect)
            x = self.get_ith_last(True, rect, i)
            return self._subtrees[i].generate_treemap(
                (x, rect[1], final_width, rect[3]))

        if not self.sum_rest_subs(i + 1):
            proportion = self._subtrees[i].data_size / self. \
                data_size
            x = self.get_ith_last(True, rect, i)
            b, c, d = rect[1], rect[2], rect[3]
            width = math.floor(proportion * c)
            new = (x, b, width, d)
            return self._subtrees[i].generate_treemap(new)

        proportion = self._subtrees[i].data_size / self. \
            data_size
        x = self.get_ith_last(True, rect, i)
        b, c, d = rect[1], rect[2], rect[3]
        width = math.floor(proportion * c)
        diff = rect[2] - (width + x)
        new = (x, b, width + diff, d)
        return self._subtrees[i].generate_treemap(new)

    def helper_subtree_height_greater(self, i: int,
                                      rect: Tuple[int, int, int, int]) \
            -> List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """ Helper for generate tree map when the height is greater than width

        and self has subtrees, returns a tuple with a rectangle and colour
        """

        if i == len(self._subtrees) - 1:
            final_height = self.find_last(False, rect)
            a, y, c, d = rect[0], rect[1], rect[2], rect[3]
            y = self.get_ith_last(False, rect, i)
            return self._subtrees[i].generate_treemap((a, y, c, final_height))

        if not self.sum_rest_subs(i + 1):
            proportion = self._subtrees[i].data_size / self. \
                data_size
            y = self.get_ith_last(False, rect, i)
            a, c, d = rect[0], rect[2], rect[3]
            height = math.floor(proportion * d)
            new = (a, y, c, height)
            return self._subtrees[i].generate_treemap(new)

        proportion = self._subtrees[i].data_size / self. \
            data_size
        y = self.get_ith_last(False, rect, i)
        a, c, d = rect[0], rect[2], rect[3]
        height = math.floor(proportion * d)
        diff = rect[3] - (height + y)
        new = (a, y, c, height + diff)
        return self._subtrees[i].generate_treemap(new)

    def base_case_width_greater(self, rect: Tuple[int, int, int, int]) \
            -> List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """ Return a tree map rectangle with colour when there is no more

        subtrees and width is greater than height.
        """
        if self == self._parent_tree._subtrees[-1]:
            return [(rect, self.colour)]

        index = self.find_position() + 1
        if not self._parent_tree.sum_rest_subs(index):
            proportion = self.data_size / self._parent_tree.data_size
            width = math.floor(proportion * rect[2])
            return [((rect[0], rect[1], width, rect[3]), self.colour)]

        width = rect[2] - rect[0]
        return [((rect[0], rect[1], width, rect[3]), self.colour
                 )]

    def base_case_height_greater(self, rect: Tuple[int, int, int, int]) \
            -> List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """ Return a tree map rectangle with colour when there is no more

        subtrees and height is greater than width.
        """

        if len(self._subtrees) == 1:
            return [(rect, self.colour)]

        if self == self._parent_tree._subtrees[-1]:
            return [(rect, self.colour)]

        index = self.find_position() + 1

        if not self._parent_tree.sum_rest_subs(index):
            proportion = self.data_size / self._parent_tree.data_size
            height = math.floor(proportion * rect[3])
            return [((rect[0], rect[1], rect[2], height), self.colour)]

        height = rect[3] - rect[1]
        return [((rect[0], rect[1], rect[2], height), self.
                 colour)]

    def find_position(self) -> int:
        """ Return the position of self in self._parent_tree.subtrees.

        Precondition: self._parent_tree is not None.

        """
        index = 0

        for subtree in self._parent_tree._subtrees:
            if subtree == self:
                return index
            index += 1

        return index

    def get_ith_last(self: AbstractTree, result: bool,
                     rect: Tuple[int, int, int, int], index: int) -> int:
        """ pass.

        """
        if result:
            data = rect[0]
            for i in range(len(self._subtrees)):

                if i == index:
                    return data

                proportion = self._subtrees[i].data_size / self.data_size
                amount = math.floor(proportion * rect[2])
                data += amount
            return data

        data = rect[1]
        for i in range(len(self._subtrees)):

            if i == index:
                return data

            proportion = self._subtrees[i].data_size / self.data_size
            amount = math.floor(proportion * rect[3])
            data += amount
        return data

    def sum_rest_subs(self, index: int) -> bool:
        """ Return True if the sum of subtrees from <index> is zero

        False otherwise
        """
        total = 0

        for subtree in self._subtrees[index:]:
            total += subtree.data_size

        return total == 0

    def find_last(self, result: bool, rect: Tuple) -> int:
        """ pass

        """
        if result:
            data_size = 0

            for i in range(len(self._subtrees)):

                if i == len(self._subtrees) - 1:
                    return rect[2] - data_size

                proportion = self._subtrees[i].data_size / self.data_size

                amount = math.floor(proportion * rect[2])
                data_size += amount
            return rect[2] - data_size

        data_size = 0
        for i in range(len(self._subtrees)):

            if i == len(self._subtrees) - 1:
                return rect[3] - data_size

            proportion = self._subtrees[i].data_size / self.data_size
            amount = math.floor(proportion * rect[3])
            data_size += amount
        return rect[3] - data_size

    def get_separator(self: AbstractTree) -> str:
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.
        """
        raise NotImplementedError

    def leaves(self) -> List[AbstractTree]:
        """ Return all leaves in self and store it in a list.

        """
        if self.is_empty():
            return []

        if not self._subtrees and self.data_size > 0:
            return [self]

        leaves = []
        for subtree in self._subtrees:
            leaves.extend(subtree.leaves())

        return leaves

    def delete_item(self, item: Any) -> bool:
        """Delete *one* occurrence of the given item from this tree.

        Return True if <item> was deleted, and False otherwise.
        Do not modify this tree if it does not contain <item>.

        """
        # Following is a modified delete_item implementation done in CSC148.

        if self.is_empty():
            # The item is not in the tree.
            return False
        if self._root == item:
            # We've found the item: now delete it.
            self._delete_root()
            return True

        for subtree in self._subtrees:
            deleted = subtree.delete_item(item)
            if deleted and subtree.is_empty():
                self._subtrees.remove(subtree)
                return True
        return False

    def _delete_root(self) -> None:
        """Delete the root of this tree.

        Precondition: this tree is non-empty.
        """
        if not self._subtrees:
            # This is a leaf. Deleting the root gives an empty tree.
            self._root = None

    def reduce_size(self: FileSystemTree, data: int) -> None:
        """ Reduces the size of every parent tree of root by the data size of
        <data>

        Precondition: <data> is a size of at least one leaf in self
        """
        if self.is_empty():
            return None

        if self._parent_tree is None:
            return None

        self._parent_tree.data_size -= data
        self._parent_tree.reduce_size(data)
        return None

    def mouse_right(self, coordinate: Tuple[int, int],
                    rect: Tuple[int, int, int, int],
                    ) -> None:
        """ Mutate the tree so the selected rectangle is removed and the tree

        size is updated for every parent tree and subtree.

        """

        if self.is_empty():
            return None

        dictionary = coordinate_leaf(self.leaves(), self.generate_treemap(rect))

        for item in dictionary:
            if coordinates_in_range(item, coordinate):
                for obj in dictionary[item]:
                    obj.reduce_size(obj.data_size)
                    obj.data_size = 0
                    self.delete_item(obj._root)
                return None

        return None

    def coordinate_to_tree(self, coordinates: Tuple[int, int],
                           rect: Tuple[int, int, int, int]) -> \
            Optional[AbstractTree]:
        """ Return the corresponding tree of a visual with <coordinates>.

        """
        dictionary = coordinate_leaf(self.leaves(), self.generate_treemap(rect))

        for item in dictionary:
            if coordinates_in_range(item, coordinates):
                return dictionary[item][0]

        return None

    def increase_decrease(self: AbstractTree, increase: bool) -> int:
        """ returns the amount <self data size> was changed by

        can be a positive or negative value.

        """
        if increase:
            added = math.ceil(self.data_size * 0.01)
            self.data_size += added
            return added

        subtracted = math.ceil(self.data_size * 0.01)
        if (self.data_size - subtracted) >= 1:
            self.data_size -= subtracted
            return subtracted

        return 0

    def increase_decrease_parent(self: AbstractTree, size: int,
                                 increase: bool) \
            -> None:
        """ Mutate the parent trees of self increasing or decreasing their size

        according to <increase>

        Precondition: self is a leaf

        """
        if increase:

            if self._parent_tree is None:
                return None

            self._parent_tree.data_size += size
            self._parent_tree.increase_decrease_parent(size, True)
            return None

        if self._parent_tree is None:
            return None

        self._parent_tree.data_size -= size
        self._parent_tree.increase_decrease_parent(size, False)
        return None

    def node_appender(self: FileSystemTree) -> List:
        """ Traverses self while concatenating nodes with the appropriate

        separator between each node using file separators.

        """
        if self.is_empty():
            return []

        if self._parent_tree is None:
            return [self._root]

        keeper = [self._root]

        keeper.extend(self._parent_tree.node_appender())

        return keeper

    def path(self: FileSystemTree) -> str:
        """ Takes a list of nodes in a file system and returns the corresponding
         path

        from root to node with the <data size> of self.

        """

        return path_to_node(self, self.node_appender()) + ' ({})' \
            .format(self.data_size)


class FileSystemTree(AbstractTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _root attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/David/csc148/assignments'

    The data_size attribute for regular files as simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self: FileSystemTree, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!

        # base case when path is a leaf (just a file)

        if not os.path.isdir(path):
            AbstractTree.__init__(self, os.path.basename(path),
                                  [], os.path.getsize(path))

        else:
            subtrees = []

            for item in os.listdir(path):
                subtrees.append(FileSystemTree(os.path.join(path, item)))

            AbstractTree.__init__(self, os.path.basename(path), subtrees)

    def get_separator(self: FileSystemTree) -> str:
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        """
        return os.path.sep


def path_to_node(tree: AbstractTree, lst: List[str]) -> str:
    """ Takes a list of nodes in a file system and returns the corresponding
     path

    from root to node.

    """
    lst.reverse()

    string = lst[0]

    for node in lst[1:]:
        string = string + tree.get_separator() + node

    return string


def coordinate_leaf(leaf: List[AbstractTree],
                    data:
                    List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]
                    ) \
        -> Dict[Tuple[int, int, int, int], List[AbstractTree]]:
    """ Return the coordinates of each leaf in a treemap.
    Precondition: length of leaf and data are the same.
    """
    tracker = {}

    i = 0

    while i < len(data):

        if data[i][0] in tracker:
            tracker[data[i][0]].append(leaf[i])
            i += 1
        else:
            tracker[data[i][0]] = [leaf[i]]
            i += 1

    return tracker


def coordinates_in_range(pos1: Tuple[int, int, int, int],
                         pos2: Tuple[int, int]) -> bool:
    """ Return True iff pos2 is in the range of pos1 False otherwise.

    """
    return pos2[0] in range(pos1[0], pos1[2] + pos1[0]) and \
        pos2[1] in range(pos1[1], pos1[3] + pos1[1])


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(
        config={
            'extra-imports': ['os', 'random', 'math'],
            'generated-members': 'pygame.*'})
