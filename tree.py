from random import randint

import pydot


class Node:
    def __init__(self, name, parent=None, children=[], data=None):
        self.parent = parent
        self.children = list(children)
        self.data = data
        self.name = name

    def as_image(self, filename):
        self.as_graph().write_png(filename)

    def as_graph(self):
        graph = pydot.Dot(graph_type="digraph")

        child_graphs = [c.as_graph() for c in self.children if c]

        for child_graph in child_graphs:
            for edge in child_graph.get_edges():
                graph.add_edge(edge)

        for child in self.children:
            if child:
                edge = pydot.Edge(src=self.name, dst=child.name)
                graph.add_edge(edge)

        return graph


class BSTNode(Node):

    def __init__(self, name, parent=None, children=[], data=None):
        super().__init__(name, parent, children, data)
        self.children = [None, None]

    @property
    def left(self):
        return self.children[0]

    @property
    def right(self):
        return self.children[1]

    def insert(self, data):
        if data < self.data:
            if self.left:
                self.left.insert(data)
            else:
                self.children[0] = BSTNode(str(data), parent=self, data=data)
                self.balance()
        if data > self.data:
            if self.right:
                self.right.insert(data)
            else:
                self.children[1] = BSTNode(str(data), parent=self, data=data)
                self.balance()

    def balance(self, from_insertion=True):
        None


class BST:
    def __init__(self, node_class=BSTNode):
        self.root = None
        self.node_class = node_class

    def insert(self, data):
        if not self.root:
            self.root = self.node_class(str(data), parent=None, children=[], data=data)
        else:
            self.root.insert(data)

    def as_image(self, filename):
        self.root.as_image(filename)


class AVLNode(BSTNode):
    def __init__(self, name, parent=None, children=[], data=None):
        super().__init__(name, parent, children, data)
        self.height = 1
        self.update_height()

    def update_height(self):
        self.height = 1
        for child in self.children:
            if child and child.height >= self.height:
                self.height = child.height + 1
        if self.parent:
            self.parent.update_height()

    def insert(self, data):
        if data < self.data:
            if self.left:
                self.left.insert(data)
            else:
                self.children[0] = AVLNode(str(data), parent=self, data=data)
                self.balance()
        if data > self.data:
            if self.right:
                self.right.insert(data)
            else:
                self.children[1] = AVLNode(str(data), parent=self, data=data)
                self.balance()

    def balance(self, from_insertion=True):
        z = self
        while z and z.children_balanced():
            z = z.parent
        if not z:
            # done, return
            self.update_height()
            return

        y = z.taller_child()
        x = y.taller_child()

        parents = [x, y, z]
        parents.sort(key=lambda x: x.data)

        subtrees = []
        for node in parents:
            for child in node.children:
                if child not in parents:
                    subtrees.append(child)

        # subtrees.sort(key=lambda x: x.data)
        a, b, c = parents
        # t0
        a.children[0] = subtrees[0]
        if subtrees[0]:
            subtrees[0].parent = a
        # t1
        a.children[1] = subtrees[1]
        if subtrees[1]:
            subtrees[1].parent = a
        # t2
        c.children[0] = subtrees[2]
        if subtrees[2]:
            subtrees[2].parent = c
        # t3
        c.children[1] = subtrees[3]
        if subtrees[3]:
            subtrees[3].parent = c

        z_parent = z.parent
        if z_parent:
            if z_parent.left == z:
                z_parent.children[0] = b
            else:
                z_parent.children[1] = b

        b.parent = z_parent
        a.parent = b
        c.parent = b
        b.children[0] = a
        b.children[1] = c

        c.update_height()
        a.update_height()
        b.update_height()
        if z_parent:
            z_parent.update_height()

    def children_balanced(self):
        if not self.left:
            return self.right.height <= 1
        elif not self.right:
            return self.left.height <= 1
        elif not self.right and not self.left:
            return True
        else:
            return abs(self.left.height - self.right.height) < 2

    def taller_child(self):
        if not self.left:
            return self.right
        elif not self.right:
            return self.left
        else:
            return self.left if self.left.height > self.right.height else self.right


class AVL(BST):
    def __init__(self, node_class=AVLNode):
        super().__init__(node_class)

    def insert(self, data):
        super().insert(data)
        while self.root.parent:
            self.root = self.root.parent


if __name__ == '__main__':
    tree = AVL()
    # for i in range(100):
    #     root.insert(randint(0, 10000))

    for i in range(4):
        tree.insert(i)

    tree.as_image("business.png")
