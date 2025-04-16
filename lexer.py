import re

# Tokens possíveis
TOKEN_SPEC = [
    ("NUMBER",     r'\d+'),
    ("ID",         r'[a-zA-Z_][a-zA-Z_0-9]*'),
    ("ASSIGN",     r'='),
    ("SEMI",       r';'),
    ("LPAREN",     r'\('),
    ("RPAREN",     r'\)'),
    ("LBRACE",     r'\{'),
    ("RBRACE",     r'\}'),
    ("PLUS",       r'\+'),
    ("MINUS",      r'-'),
    ("MULT",       r'\*'),
    ("DIV",        r'/'),
    ("EQ",         r'=='),
    ("NEQ",        r'!='),
    ("LT",         r'<'),
    ("GT",         r'>'),
    ("LE",         r'<='),
    ("GE",         r'>='),
    ("WHITESPACE", r'[ \t\n]+'),
    ("UNKNOWN",    r'.'),
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)

def lexer(code):
    tokens = []
    for match in re.finditer(TOKEN_REGEX, code):
        kind = match.lastgroup
        value = match.group()
        if kind == "WHITESPACE":
            continue
        elif kind == "UNKNOWN":
            raise SyntaxError(f"Caractere inválido: {value}")
        tokens.append((kind, value))
    return tokens
