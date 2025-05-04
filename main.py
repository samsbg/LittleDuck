import ply.lex as lex

from CustomLexer import CustomLexer
from CustomParser2 import CustomParser2


# Custom compiler

customLexer = CustomLexer()

print('\n3.3 - Tokeniza con Ply')

print('\n-----------------------------------------\n')

# Abre el archivo y procesa el programa por el lexer
with open("Samples/sample_asignaciones.ld", "r") as file:
    for index, line in enumerate(file):

        dataTemp = line

        lineTokens = customLexer.analisis(dataTemp)

        lineTokens.add_token('EOL', 'EOL', len(dataTemp), 0)

        CustomParser2(lineTokens, 'ASSIGN')

        lineTokens.print_linea()
        lineTokens.print_errors()
