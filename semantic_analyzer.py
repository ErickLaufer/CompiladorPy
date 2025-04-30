from symbol_table import SymbolTable
from ast_nodes import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.analyze(stmt)

        elif isinstance(node, VarDecl):
            if self.symbol_table.lookup(node.identifier):
                raise Exception(f"Erro semântico: variável '{node.identifier}' já declarada.")
            self.symbol_table.declare(name=node.identifier, kind="variável", type_=node.var_type)
            self.analyze(node.value)

        elif isinstance(node, Assignment):
            symbol = self.symbol_table.lookup(node.identifier)
            if not symbol:
                raise Exception(f"Erro semântico: variável '{node.identifier}' não declarada antes do uso.")
            self.analyze(node.value)

        elif isinstance(node, BinaryOp):
            self.analyze(node.left) # Analisar o lado esquerdo da operação binária
            self.analyze(node.right) # Analisar o lado direito da operação binária

        elif isinstance(node, Number):
            # return "int" #retornar o tipo do número
            pass  # Nada a verificar

        elif isinstance(node, Identifier):
            symbol = self.symbol_table.lookup(node.name)
            if not symbol:
                raise Exception(f"Erro semântico: variável '{node.name}' usada sem declaração.")

        else:
            raise Exception(f"Erro semântico: nó desconhecido {type(node)}")
