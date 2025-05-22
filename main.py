from lexer import lexer
from parser import Parser
from utils import print_ast
from semantic_analyzer import SemanticAnalyzer

def main():
    codigo_fonte = """
int x = 10;
float y = 3.14;
string nome = "João";
boolean ativo = true;

x = 1 + 5 + x + nome;
y = y + 0.01;

    """

# REALIZAR TESTE DE FUNÇÃO COM VALIDAÇÔES DE PARAMETROS E RETORNOS 
# RESOLVER EXPRESSAO ARITMETICA COM ()

    print(">>> Código Fonte:")
    print(codigo_fonte)

    try:
        tokens = lexer(codigo_fonte)
        print("\n>>> Tokens:")
        for token in tokens:
            print(token)

        parser = Parser(tokens)
        ast = parser.parse()

        print("\n>>> AST (formatada):")
        print_ast(ast)

        print("\n>>> Análise Semântica:")
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        print("✅ Sem erros semânticos detectados.")

    except Exception as e:
        print(f"❌ {e}")

if __name__ == "__main__":
    main()
