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
            return "boolean"
    
        elif isinstance(node, FunctionDecl):
            if self.symbol_table.lookup(node.name):
                raise Exception(f"Erro semântico: função '{node.name}' já declarada.")

            self.symbol_table.declare(name=node.name, kind="função", type_=node.return_type)
            self.symbol_table.push_scope()

            for param_name, param_type in node.parameters:
                if self.symbol_table.lookup(param_name):
                    raise Exception(f"Erro semântico: parâmetro '{param_name}' duplicado.")
                self.symbol_table.declare(name=param_name, kind="parâmetro", type_=param_type)

            for stmt in node.body:
                retorno = self.analyze(stmt)
                if isinstance(stmt, Return) and retorno != node.return_type:
                    raise Exception(f"Erro semântico: retorno incompatível na função '{node.name}'. Esperado '{node.return_type}', obtido '{retorno}'.")

            self.symbol_table.pop_scope()

        elif isinstance(node, FunctionCall):
            symbol = self.symbol_table.lookup(node.name)
            if not symbol or symbol.kind != "função":
                raise Exception(f"Erro semântico: função '{node.name}' não declarada.")

            for arg in node.arguments:
                self.analyze(arg)  # Aqui poderia validar tipos se você armazenasse os parâmetros da função

            return symbol.type  # Retorna tipo da função para validação em atribuições

        elif isinstance(node, Return):
            return self.analyze(node.value)

        else:
            raise Exception(f"Erro semântico: nó desconhecido {type(node)}")

        
