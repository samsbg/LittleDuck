from TokenDef import token_equivalentes

parse_table = {}

parse_table['ASSIGN'] = {}
parse_table['EXPRESSION'] = {}
parse_table['EXP'] = {}
parse_table['EXPRESION_PRIME'] = {}
parse_table['EXP_PRIME'] = {}
parse_table['OL'] = {}
parse_table['TERMINO'] = {}
parse_table['TERMINO_PRIME'] = {}
parse_table['FACTOR'] = {}
parse_table['ID_NUMBER'] = {}
parse_table['CTE'] = {}

parse_table['ASSIGN']['IDENTIFICADOR'] = ['IDENTIFICADOR', 'OA_IGUAL', 'EXPRESSION', 'DEL_PUYCO']

for op in ['DEL_PARABI', 'OA_SUMA', 'OA_RESTA', 'IDENTIFICADOR', 'CA_NUMBER', 'CA_FLOAT']:
    parse_table['EXPRESSION'][op] = ['EXP', 'EXPRESION_PRIME']
    parse_table['EXP'][op] = ['TERMINO', 'EXP_PRIME']
    parse_table['TERMINO'][op] = ['FACTOR', 'TERMINO_PRIME']

for op in ['DEL_FLEIZQ', 'DEL_FLEDER', 'OL_NOIGU', 'OL_IGUIGU', 'OL_MEIGU', 'OL_MAIGU']:
    parse_table['EXPRESION_PRIME'][op] = [op, 'EXP']
    parse_table['EXP_PRIME'][op] = ['e']
    parse_table['TERMINO_PRIME'][op] = ['e']

for op in ['DEL_PUYCO', 'DEL_PARCER']:
    parse_table["EXPRESION_PRIME"][op] = ['e']
    parse_table["EXP_PRIME"][op] = ['e']
    parse_table["TERMINO_PRIME"][op] = ['e']

parse_table['EXPRESION_PRIME']['$'] = []

parse_table["EXP_PRIME"]['OA_SUMA'] = ['OA_SUMA', 'TERMINO', "EXP_PRIME"]
parse_table["EXP_PRIME"]['OA_RESTA'] = ['OA_RESTA', 'TERMINO', "EXP_PRIME"]

parse_table["TERMINO_PRIME"]['OA_SUMA'] = ['e']
parse_table["TERMINO_PRIME"]['OA_RESTA'] = ['e']
parse_table["TERMINO_PRIME"]['OA_MULTI'] = ['OA_MULTI', 'FACTOR', "TERMINO_PRIME"]
parse_table["TERMINO_PRIME"]['OA_DIVI'] = ['OA_DIVI', 'FACTOR', "TERMINO_PRIME"]

parse_table['FACTOR']['DEL_PARABI'] = ['DEL_PARABI', 'EXPRESSION', 'DEL_PARCER']
parse_table['FACTOR']['OA_SUMA'] = ['OA_SUMA', 'ID_NUMBER']
parse_table['FACTOR']['OA_RESTA'] = ['OA_RESTA', 'ID_NUMBER']
parse_table['FACTOR']['IDENTIFICADOR'] = ['IDENTIFICADOR']
parse_table['FACTOR']['CA_NUMBER'] = ['CA_NUMBER']
parse_table['FACTOR']['CA_FLOAT'] = ['CA_FLOAT']

parse_table['ID_NUMBER']['IDENTIFICADOR'] = ['IDENTIFICADOR']
parse_table['ID_NUMBER']['CTE'] = ['CTE']

parse_table['CTE']['CA_NUMBER'] = ['CA_NUMBER']
parse_table['CTE']['CA_FLOAT'] = ['CA_FLOAT']

def CustomParser2(input_tokens, start):
    stack = ['EOL', start]
    tokens = input_tokens.tokens.copy()

    while stack:
        top = stack.pop()
        current = tokens[0]
        current_token = current.token

        if top == current_token:
            tokens.pop(0)
        elif top in parse_table and current_token in parse_table[top]:
            production = parse_table[top][current_token]
            for symbol in reversed(production):
                if symbol != 'e':
                    stack.append(symbol)
        else:
            if (parse_table.get(top) is None):
                expected = token_equivalentes.get(top)
            else:
                expected = [token_equivalentes.get(token) for token in list(parse_table[top].keys())]
                
            input_tokens.lista_errores.append(f"ERROR SINTAX en linea {current.lineaPos} index {current.lexpos}. Se encontró {current.content} dentro de la gramatica {top}. Se esperaba {expected}")
            break
