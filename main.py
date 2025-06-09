import ply.lex as lex

from CustomLexer import CustomLexer
from CustomParser import CustomParser
from CustomVM import VM

from TokenDef import Tokens

# Custom compiler

customLexer = CustomLexer()
customParser = CustomParser()

tokensDoc = Tokens(0, '')

print('\nEntrega 4')

print('\n-----------------------------------------\n')

# Abre el archivo y procesa el programa por el lexer
with open("Samples/sample13.ld", "r") as file:

    lineCount = 1

    for index, line in enumerate(file):

        lineTokens = customLexer.analisis(line)
        tokensDoc.add_tokens(lineTokens)

        lineCount += 1

    tokensDoc.add_token('EOD', 'EOD', 0, lineCount)

    customParser.analisis(tokensDoc)

    tokensDoc.program_valid()
    tokensDoc.print_errors()

    if (customParser.listaCuadruples.programaValido()):
        customParser.listaCuadruples.imprimir_archivo()

        customVM = VM()
        customVM.analisis()
