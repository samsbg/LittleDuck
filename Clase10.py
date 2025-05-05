
import ply.lex as lex    # importa lex
import ply.yacc as yacc  # importa yacc

#from my_lexer_file import tokens, lexer
from TokenDef import Tokens, reserved, alfanumericos, token_patterns

tokens = [
    'IDENTIFICADOR', 'NEWLINE'
] + alfanumericos + list(token_patterns.keys()) + list(
    reserved.values())

# Dynamically assign token regexes to module-level variables
for token_name, pattern in token_patterns.items():
    exec(f't_{token_name} = r"""{pattern}"""')

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')
    return t

def t_CA_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CA_FLOAT(t):
    r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer

lexer = lex.lex()

#------------------------------------------------

# # Parsing rules

precedence = (
    ('left', 'OL_OR'),
    ('left', 'OL_AND'),
    ('nonassoc', 'OL_IGUIGU', 'OL_NOIGU'),
    ('nonassoc', 'OL_MEIGU', 'OL_MAIGU'),
    ('nonassoc', 'DEL_FLEIZQ', 'DEL_FLEDER'),
)

# diccionario de nombres
names = { }



#--------------------------------------------------------

# p_ functions here.... : P 

def p_statement(t):
    '''statement : statement statement
                 | asigna'''

def p_asigna(t):
    'asigna : IDENTIFICADOR OA_IGUAL expresion DEL_PUYCO'
    names[t[1]] = t[3]

def p_expresion(t):
    '''expresion : exp DEL_FLEIZQ exp
                 | exp DEL_FLEDER exp
                 | exp OL_NOIGU exp
                 | exp OL_IGUIGU exp
                 | exp OL_MEIGU exp
                 | exp OL_MAIGU exp
                 | exp OL_AND exp
                 | exp OL_OR exp
                 | exp'''

    if len(t) == 4:
        if t[2] == '<':
            t[0] = t[1] < t[3]
        elif t[2] == '>':
            t[0] = t[1] > t[3]
        elif t[2] == '==':
            t[0] = t[1] == t[3]
        elif t[2] == '!=':
            t[0] = t[1] != t[3]
        elif t[2] == '<=':
            t[0] = t[1] <= t[3]
        elif t[2] == '>=':
            t[0] = t[1] >= t[3]
        elif t[2] == '&&':
            t[0] = t[1] and t[3]
        elif t[2] == '||':
            t[0] = t[1] or t[3]
    else:
        t[0] = t[1]

def p_exp(t):
    '''exp : exp OA_SUMA termino
           | exp OA_RESTA termino
           | termino'''
    if len(t) == 4:
        if t[2] == '+':
            t[0] = t[1] + t[3]
        elif t[2] == '-':
            t[0] = t[1] - t[3]
    else:
        t[0] = t[1]

def p_termino(t):
    '''termino : termino OA_MULTI factor
               | termino OA_DIVI factor
               | factor'''
    if len(t) == 4:
        if t[2] == '*':
            t[0] = t[1] * t[3]
        elif t[2] == '/':
            t[0] = t[1] / t[3]
    else:
        t[0] = t[1]

def p_factor(t):
    '''factor : cte
              | IDENTIFICADOR
              | DEL_PARABI expresion DEL_PARCER'''
    if len(t) == 2:
        if names.get(t[1]):
            t[0] = names[t[1]]
        else:     
            t[0] = t[1]
    else:
        t[0] = t[2] 

def p_cte(t):
    '''cte : CA_NUMBER
           | CA_FLOAT'''
    t[0] = t[1]

def p_error(t):
    print("Syntax error at '%s'" % t.value)


parser = yacc.yacc()

s = """ 
    b = 15 + 15 * 2 ;  
    otra_var = b + 15 ; 
"""
#s = """b = 15+15*2;  otra_var = b + 15;  """

result = parser.parse(s)

print(result)
print(names)