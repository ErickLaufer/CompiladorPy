from symbol_table import SymbolTable

def teste_simbolos():
    tabela = SymbolTable()

    # Escopo global
    tabela.declare('x', kind='variável', type_='int')

    print("Escopo global:", tabela.scopes)

    # Entra num novo escopo (ex: dentro de função)
    tabela.enter_scope()
    tabela.declare('y', kind='variável', type_='int')

    print("Escopo interno:", tabela.scopes)

    # Verificações
    print("Buscar 'x':", tabela.lookup('x'))  # Deve encontrar
    print("Buscar 'y':", tabela.lookup('y'))  # Deve encontrar

    tabela.exit_scope()
    print("Após sair do escopo interno:", tabela.scopes)
    print("Buscar 'y' após sair:", tabela.lookup('y'))  # Deve ser None

teste_simbolos()
