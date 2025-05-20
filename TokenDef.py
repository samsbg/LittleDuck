import re
import time

BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

reserved = {
    'if': 'PR_IF',
    'else': 'PR_ELSE',
    'while': 'PR_WHILE',
    'for': 'PR_FOR',
    'print': 'PR_PRINT',
    'true': 'PR_TRUE',
    'false': 'PR_FALSE',
    'do': 'PR_DO',
    'var': 'PR_VAR',
    'const': 'PR_CONST',
    'int': 'PR_INT',
    'program': 'PR_PROGRAM',
    'main': 'PR_MAIN',
    'end': 'PR_END',
    'string': 'PR_STRING',
    'void': 'PR_VOID',
    'float': 'PR_FLOAT',
}

alfanumericos = ['CA_NUMBER', 'CA_FLOAT', 'CA_STRING']

token_patterns = {
    # Aritmeticos
    'OA_SUMA': r'\+',
    'OA_RESTA': r'-',
    'OA_MULTI': r'\*',
    'OA_DIVI': r'/',
    'OA_IGUAL': r'=',
    # Logicos
    'OL_AND': r'&&',
    'OL_OR': r'\|\|',
    'OL_IGUIGU': r'==',
    'OL_NOIGU': r'!=',
    'OL_MAIGU': r'>=',
    'OL_MEIGU': r'<=',
    # Delimitadores
    'DEL_COMA': r',',
    'DEL_PARABI': r'\(',
    'DEL_PARCER': r'\)',
    'DEL_BRAABI': r'\[',
    'DEL_BRACER': r'\]',
    'DEL_CORABI': r'\{',
    'DEL_CORCER': r'\}',
    'DEL_FLEIZQ': r'<',
    'DEL_FLEDER': r'>',
    'DEL_DOSPU': r':',
    'DEL_PUYCO': r';'
}

token_equivalentes = {'IDENTIFICADOR': 'id', 'CA_NUMBER': 'numero', 'CA_FLOAT': 'float', 'CA_STRING': 'string'}

token_equivalentes.update({
    key: re.sub(r'\\', '', value)
    for key, value in token_patterns.items()
})

token_equivalentes.update({v: k for k, v in reserved.items()})

class Token:
    # Atributos
    token = ""
    content = ""
    lexpos = 0
    lineaPos = 0

    # Constructor de la clase...
    def __init__(self, token, content, lexpos, lineaPos):
        self.token = token
        self.content = content
        self.lexpos = lexpos
        self.lineaPos = lineaPos

    def print_token_ext(self):
        if (self.token == 'ERROR'):
            print(f"{BOLD}Símbolo o palabra no reconocido: {RESET}{self.content[0]} at lexpos: {self.lexpos}")
            return

        if (self.token == 'EOD'):
            return

        type = f"{self.token:<{18}}"
        value = f"{'value: ' + str(self.content):<{20}}"
        lexpos = 'lexpos: ' + str(self.lexpos)

        print(type + value + lexpos)
            

# Una clase tokens basica...
class Tokens:
  # Atributos
    tokens = []
    lineaPos = 0
    cadena = ''
    
    pos = 0
    
    lista_errores = []
    tabla_simbolos = {}

    # Constructor de la clase...
    def __init__(self, lineaPos, cadena):
        self.tokens = []
        self.lineaPos = lineaPos
        self.pos = 0
        self.lista_errores = []
        self.cadena = cadena

    def add_token(self, token, content, lexpos, lineaPos):
        currToken = Token(token, content, lexpos, lineaPos)
        self.tokens.append(currToken)

    def add_tokens(self, tokensInput):
        self.tokens.extend(tokensInput.tokens)
        self.lista_errores.extend(tokensInput.lista_errores)
        self.add_tabla_simbolos(tokensInput.tabla_simbolos)

    def add_tabla_simbolos(self, tablaInput):
        for key, value in tablaInput.items():
            if key in self.tabla_simbolos:
                self.tabla_simbolos[key].extend(value)
            else:
                self.tabla_simbolos[key] = value.copy()

    def current(self):
        return self.tokens[self.pos]

    def peek(self):
        return self.tokens[self.pos+1]

    def avanza(self):
        if (self.current().token != 'EOD'):
            self.pos += 1
        return self.tokens[self.pos]

    def print_tokens(self):
        for tok in self.tokens:
            tok.print_token_ext()
    
    def print_linea(self):
        if (len(self.tokens) == 0):
            return
        
        if (len(self.lista_errores) == 0):
            print(f"\n{BOLD}Linea {self.lineaPos}: {RESET}{GREEN}OKS - '{self.cadena}'{RESET}")
        else:
            print(f"\n{BOLD}Linea {self.lineaPos}: {RESET}{RED}NOPE - '{self.cadena}'{RESET}")

        print(', '.join(f"[{t.token}, {t.content}]" for t in self.tokens[:-1]))
        self.print_tokens()

    def program_valid(self):
        if (len(self.lista_errores) == 0):
            print(f"{GREEN}\nOKS - Programa válido{RESET}\n\n")
        else:
            print(f"{RED}\nNOPE - Programa no válido{RESET}\n\n")

    def print_errors(self):
        if (len(self.lista_errores) != 0):
            for error in self.lista_errores:
                print(error)
            print()

    def print_tabla_simbolos(self):
        print(f'{BOLD}Tabla de símbolos [Línea, Posición]{RESET}')
        for element, value in self.tabla_simbolos.items():
            print(f"{element:<{20}}{value}")

class Estructura_Impresion:
    def __init__(self):
        self.stack = []

    def empezar_estructura(self, name):
        indent = '|    ' * len(self.stack)
        print(f"{indent}{name}")
        self.stack.append(name)

    def termina_estructura(self):
        self.stack.pop()
        indent = '|    ' * len(self.stack)
        print(f"{indent}>")

    def marcar_error(self):
        indent = '|    ' * len(self.stack)
        print(f"{indent}ERROR!")
