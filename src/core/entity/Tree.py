import json


class Tree:
    def __init__(self):
        super(Tree, self).__init__()

class ExNode(Tree):
    def __init__(self, _size):
        # super(ExNode, self).__init__()
        self._size = _size

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, _size):
        self._size = _size

class InNode(Tree):
    def __init__(self, _left, _right, _split_att, _split_value):
        # super(InNode, self).__init__()
        self._left = _left
        self._right = _right
        self._split_att = _split_att
        self._split_value = _split_value

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self,_left):
        self._left = _left

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self,_right):
        self._right = _right

    @property
    def split_att(self):
        return self._split_att

    @split_att.setter
    def split_att(self,_split_att):
        self._split_att = _split_att

    @property
    def split_value(self):
        return self._split_value

    @split_value.setter
    def split_value(self,_split_value):
        self._split_value = _split_value
