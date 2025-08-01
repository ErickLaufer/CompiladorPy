from ast_nodes import *
from lexer import lexer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')

    def eat(self, expected_type):
        if self.current()[0] == expected_type:
            self.pos += 1
        else:
            raise SyntaxError(f"Esperado {expected_type}, encontrado {self.current()[0]}")
        
    def peek(self):
        return self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else ('EOF', '')

    def parse(self):
        statements = []
        while self.current()[0] != 'EOF':
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
        token_type, value = self.current()

        if token_type == 'ID' and value in ('int', 'float', 'string', 'boolean'):
            return self.var_decl()
        if token_type == 'FUNCTION':
            return self.function_decl()
        elif token_type == 'ID':
            return self.assignment()
        elif token_type == 'IF':
            return self.if_statement()
        else:
            raise SyntaxError(f"Comando inválido: {token_type}")
        
    def function_call(self):
        name = self.current()[1]
        self.eat('ID')
        self.eat('LPAREN')
        args = []

        if self.current()[0] != 'RPAREN':
            while True:
                args.append(self.expression())
                if self.current()[0] == 'COMMA':
                    self.eat('COMMA')
                else:
                    break

        self.eat('RPAREN')
        return FunctionCall(name, args)


    def var_decl(self):
        tipo_token = self.current()
        self.eat('ID')  # tipo (ex: int, float, string, boolean)
        var_type = tipo_token[1]  # 'int', 'float', 'string', 'boolean'

        identifier = self.current()[1]
        self.eat('ID')

        self.eat('ASSIGN')
        value = self.expression()
        self.eat('SEMI')
        return VarDecl(var_type, identifier, value)

    def assignment(self):
        identifier = self.current()[1]
        self.eat('ID')
        self.eat('ASSIGN')
        value = self.expression()
        self.eat('SEMI')
        return Assignment(identifier, value)

    def expression(self):
        left = self.term()
        while self.current()[0] in ('PLUS', 'MINUS'):
            op = self.current()[1]
            self.eat(self.current()[0])
            right = self.term()
            left = BinaryOp(left, op, right)
        return left

    def term(self):
        token_type, value = self.current()

        if token_type == 'NUMBER':
            self.eat('NUMBER')
            return Number(value)

        elif token_type == 'FLOAT':
            self.eat('FLOAT')
            return Float(value)

        elif token_type == 'STRING':
            self.eat('STRING')
            return String(value)

        elif token_type == 'BOOL':
            self.eat('BOOL')
            return Boolean(value)
        
        elif token_type == 'ID':
            if self.peek()[0] == 'LPAREN':
                return self.function_call()
            else:
                self.eat('ID')
                return Identifier(value)
        elif token_type == 'ID':
            self.eat('ID')
            return Identifier(value)
        else:
            raise SyntaxError(f"Expressão inválida com token: {token_type}")
# Testando o parser

    def function_decl(self):
        self.eat('FUNCTION')
        return_type = self.current()[1]
        self.eat('ID')  # tipo de retorno

        name = self.current()[1]
        self.eat('ID')  # nome da função

        self.eat('LPAREN')
        parameters = []

        if self.current()[0] != 'RPAREN':
            while True:
                param_type = self.current()[1]
                self.eat('ID')
                param_name = self.current()[1]
                self.eat('ID')
                parameters.append((param_name, param_type))
                if self.current()[0] == 'COMMA':
                    self.eat('COMMA')
                else:
                    break

        self.eat('RPAREN')
        self.eat('LBRACE')
        body = []

        while self.current()[0] != 'RBRACE':
            if self.current()[0] == 'RETURN':
                self.eat('RETURN')
                value = self.expression()
                self.eat('SEMI')
                body.append(Return(value))
            else:
                body.append(self.statement())

        self.eat('RBRACE')
        return FunctionDecl(name, parameters, body, return_type)
    
    def if_statement(self):
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.expression()
        self.eat('RPAREN')

        self.eat('LBRACE')
        true_block = []
        while self.current()[0] != 'RBRACE':
            true_block.append(self.statement())
        self.eat('RBRACE')

        false_block = None
        if self.current()[0] == 'ELSE':
            self.eat('ELSE')
            self.eat('LBRACE')
            false_block = []
        while self.current()[0] != 'RBRACE':
            false_block.append(self.statement())
        self.eat('RBRACE')
        return IfStatement(condition, true_block, false_block)
