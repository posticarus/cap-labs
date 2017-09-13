from AritPlotLexer import AritPlotLexer
from AritPlotParser import AritPlotParser
from MyAritPlotVisitor import MyAritPlotVisitor, UnknownIdentifier

from LibDraw import LibDraw
from antlr4 import FileStream, CommonTokenStream
import sys

# mini project 2017 : plot !

debug = False


def main():
    # Suppose that an input file always exists.
    lexer = AritPlotLexer(FileStream(sys.argv[1]))
    stream = CommonTokenStream(lexer)
    parser = AritPlotParser(stream)
    tree = parser.prog()
    if debug:
        print("Parsing : done.")
    # Launch the Visitor !
    myg = LibDraw(200, 300, True)
    visitor = MyAritPlotVisitor(myg, False)  # True for debug mode
    try:
        visitor.visit(tree)
    except UnknownIdentifier as exc:  # Visitor's exception
        print('Unknown identifier: {}'.format(exc.args[0]))
        exit(-1)

if __name__ == '__main__':
    main()
