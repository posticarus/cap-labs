from antlr4 import InputStream
from antlr4 import CommonTokenStream

# include to use the generated lexer and parser
from Exemple2Lexer import Exemple2Lexer
from Exemple2Parser import Exemple2Parser

import sys


def main():
    input_stream = InputStream(sys.stdin.read())
    lexer = Exemple2Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Exemple2Parser(stream)
    parser.r()
    print("Finished")

# warns pb if py file is included in others
if __name__ == '__main__':
    main()
