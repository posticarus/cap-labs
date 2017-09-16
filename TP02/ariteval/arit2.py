from Arit2Lexer import Arit2Lexer
from Arit2Parser import Arit2Parser
import antlr4
import sys


def main():
    lexer = Arit2Lexer(antlr4.InputStream(sys.stdin.read()))
    stream = antlr4.CommonTokenStream(lexer)
    parser = Arit2Parser(stream)
    parser.prog()

if __name__ == '__main__':
    main()
