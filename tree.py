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
        graph = pydot.Dot(graph_type="graph")

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
        if data > self.data:
            if self.right:
                self.right.insert(data)
            else:
                self.children[1] = BSTNode(str(data), parent=self, data=data)


class BST:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if not self.root:
            self.root = BSTNode(str(data), parent=None, children=[], data=data)
        else:
            self.root.insert(data)

    def as_image(self, filename):
        self.root.as_image(filename)


if __name__ == '__main__':
    root = BST()
    for i in range(100):
        root.insert(randint(0, 10000))

    root.as_image("business.png")
