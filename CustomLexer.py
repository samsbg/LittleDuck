import ply.lex as lex

from TokenDef import Tokens, reserved, alfanumericos, token_patterns

BOLD = "\033[1m"
RESET = "\033[0m"

class CustomLexer:
    tokens = [
        'IDENTIFICADOR', 'NEWLINE'
    ] + alfanumericos + list(token_patterns.keys()) + list(
        reserved.values())

    # Dynamically assign token regexes to module-level variables
    for token_name, pattern in token_patterns.items():
        exec(f't_{token_name} = r"""{pattern}"""')

    t_ignore = ' \t'
    t_ignore_COM_SL = r'\#.*'
    t_ignore_COM_ML = r'\/\*[\s\S]*?\*\/'

    def __init__(self):        
        self.lexer = lex.lex(module=self)

    def analisis(self, cadena):
        self.errores = []
        self.tabla_simbolos = {}
        self.lexer.input(cadena)
        
        tokens = Tokens(self.lexer.lineno, cadena.strip())

        for tok in self.lexer:
            tokens.add_token(tok.type, tok.value, tok.lexpos, self.lexer.lineno)

        tokens.lista_errores = self.errores
        tokens.tabla_simbolos = self.tabla_simbolos

        return tokens

    def error_string(self, simbolo, lineno, lexpos):
        return f"ERROR LEXICO en linea {lineno} index {lexpos}: Símbolo o palabra no reconocido: {simbolo}"

    def t_IDENTIFICADOR(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'IDENTIFICADOR')
        if t.type == 'IDENTIFICADOR':
            if t.value not in self.tabla_simbolos:
                self.tabla_simbolos[t.value] = []
            self.tabla_simbolos[t.value].append([t.lineno, t.lexpos])
        return t

    def t_CA_FLOAT(self, t):
        r'[+-]?(\d+\.\d*|\.\d+)([eE][+-]?\d+)?'
        t.value = float(t.value)
        return t
    
    def t_CA_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_CA_STRING(self, t):
        r'"[^"]*"'
        t.value = t.value[1:-1]  # remove quotes
        return t

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        t.type = 'ERROR'
        t.value = t.value[0]
        error = self.error_string(t.value, t.lineno, t.lexpos)
        self.errores.append(error)
        t.lexer.skip(1)
        
        return t
