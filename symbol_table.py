class Symbol:
    def __init__(self, name, kind, type_, scope_level):
        self.name = name
        self.kind = kind  # variável ou função
        self.type = type_
        self.scope_level = scope_level

    def __repr__(self):
        return f"<{self.kind} {self.name}:{self.type} (escopo {self.scope_level})>"

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # lista de dicionários, um por escopo
        self.scope_level = 0

    def enter_scope(self):
        self.scope_level += 1
        self.scopes.append({})

    def exit_scope(self):
        if self.scope_level > 0:
            self.scopes.pop()
            self.scope_level -= 1

    def declare(self, name, kind, type_):
        current_scope = self.scopes[-1]
        if name in current_scope:
            raise Exception(f"Erro: '{name}' já declarado no escopo atual.")
        current_scope[name] = Symbol(name, kind, type_, self.scope_level)

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
    def push_scope(self):
        self.enter_scope()

    def pop_scope(self):
        self.exit_scope()
    
        return None  # não encontrado 
