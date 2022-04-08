class Node:
    def __init__(self, value=None, *nodes):
        self.value = value
        self.children = []
        self.addChildren(nodes)

    def setValue(self, value):
        self.value = value
    
    def addChildren(self, *nodes):
        for child in nodes:
            if not isinstance(child, Node):
                raise RuntimeError("Child must be of type Node")
            self.children.append(child)

    def getValue(self):
        return self.value

    def getChildren(self):
        return self.children

class AST:
    def __init__(self, root:Node=None):
        self.root = root
    

def main():
    n1 = Node(value=5)
    n2 = Node(10, leftChild=n1, rightChild=Node(7))
    n1.setLeftChild(Node(11))


main()
    



    