from lexer import lexer
from parser import Parser
from utils import print_ast
from semantic_analyzer import SemanticAnalyzer
from tac_generator import TACGenerator
from assembly_generator import AssemblyGenerator   


def main():
    codigo_fonte = """
function int soma(int a, int b) {
    return a + b;
}

int resultado = soma(3, 4);

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

    print("\n>>> Código TAC:")
    tac = TACGenerator()
    tac.generate(ast)
    print(tac.dump())
    print("\n>>> Código Assembly:")
    asm = AssemblyGenerator(tac.dump())
    print(asm.generate())

if __name__ == "__main__":
    main()
