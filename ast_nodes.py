# ast_nodes.py

class Node:
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class VarDecl(Node):
    def __init__(self, var_type, identifier, value):
        self.var_type = var_type
        self.identifier = identifier
        self.value = value

class Assignment(Node):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

class BinaryOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(Node):
    def __init__(self, value):
        self.value = int(value)

class Identifier(Node):
    def __init__(self, name):
        self.name = name
