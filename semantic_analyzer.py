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
            expr_type = self.analyze(node.value)
            self.symbol_table.declare(name=node.identifier, kind="variável", type_=node.var_type)
            if expr_type != node.var_type:
                raise Exception(f"Erro semântico: tipo incompatível na inicialização de '{node.identifier}'. Esperado '{node.var_type}', encontrado '{expr_type}'.")

        elif isinstance(node, Assignment):
            symbol = self.symbol_table.lookup(node.identifier)
            if not symbol:
                raise Exception(f"Erro semântico: variável '{node.identifier}' não declarada antes do uso.")
            expr_type = self.analyze(node.value)
            if expr_type != symbol.type:
                raise Exception(f"Erro semântico: tipo incompatível na atribuição para '{node.identifier}'. Esperado '{symbol.type}', encontrado '{expr_type}'.")

        elif isinstance(node, BinaryOp):
            left_type = self.analyze(node.left)
            right_type = self.analyze(node.right)
            if left_type != right_type:
                raise Exception(f"Erro semântico: operação binária com tipos incompatíveis: '{left_type}' e '{right_type}'")
            return left_type  # Assume que o tipo da operação é o mesmo dos operandos

        elif isinstance(node, Number):
            return "int"

        elif isinstance(node, Identifier):
            symbol = self.symbol_table.lookup(node.name)
            if not symbol:
                raise Exception(f"Erro semântico: variável '{node.name}' usada sem declaração.")
            return symbol.type
            
        elif isinstance(node, Float):
            return "float"
        
        elif isinstance(node, String):
            return "string"
        
        elif isinstance(node, Boolean):
            return "bool"
            
        else:
            raise Exception(f"Erro semântico: nó desconhecido {type(node)}")
        
