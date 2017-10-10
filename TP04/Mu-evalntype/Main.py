from MuLexer import MuLexer
from MuParser import MuParser
from MyMuVisitor import MyMuVisitor, MuRuntimeError, MuSyntaxError
from MyMuTypingVisitor import MyMuTypingVisitor, MuTypeError

import argparse
import antlr4

# Main file for Lab 4, CAP, october 2017

enable_typing = False

def main():
    # command line
    parser = argparse.ArgumentParser(description='Exec/Type mu files.')
    parser.add_argument('path', type=str,
                        help='file to exec and type')
    args = parser.parse_args()

    # lex and parse
    input_s = antlr4.FileStream(args.path)
    lexer = MuLexer(input_s)
    stream = antlr4.CommonTokenStream(lexer)
    parser = MuParser(stream)
    tree = parser.prog()

    # typing Visitor
    if enable_typing:
        visitor1 = MyMuTypingVisitor()
        try:
            visitor1.visit(tree)
        except MuTypeError as e:
            print(e.args[0])
            exit(1)

    # eval Visitor
    visitor2 = MyMuVisitor()
    try:
        visitor2.visit(tree)
    except (MuRuntimeError, MuSyntaxError) as e:
        print(e.args[0])
        exit(1)

if __name__ == '__main__':
    main()
