import ply.lex as lex

from CustomLexer import CustomLexer
from CustomParser import CustomParser

from TokenDef import Tokens


# Custom compiler

customLexer = CustomLexer()
customParser = CustomParser()

tokensDoc = Tokens(0, '')

print('\n3.3 - Tokeniza con Ply')

print('\n-----------------------------------------\n')

# Abre el archivo y procesa el programa por el lexer
with open("Samples/sample5.ld", "r") as file:

    lineCount = 1

    for index, line in enumerate(file):

        lineTokens = customLexer.analisis(line)
        tokensDoc.add_tokens(lineTokens)

        lineCount += 1

    tokensDoc.add_token('EOD', 'EOD', 0, lineCount)

    customParser.analisis(tokensDoc)

    tokensDoc.program_valid()
    tokensDoc.print_errors()
