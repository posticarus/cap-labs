#! /usr/bin/env python3
"""
Usage:
    python3 arit.py <filename>
"""

from AritPlotLexer import AritPlotLexer
from AritPlotParser import AritPlotParser
from MyAritPlotVisitor import MyAritPlotVisitor, UnknownIdentifier

from LibDraw import LibDraw
from antlr4 import FileStream, CommonTokenStream
import sys

import argparse

# mini project 2017 : plot !

debug = True


def main(inputname, nopict=False):
    lexer = AritPlotLexer(FileStream(inputname))
    stream = CommonTokenStream(lexer)
    parser = AritPlotParser(stream)
    tree = parser.prog()
    # Launch the Visitor !
    myg = LibDraw(200, 300, True, nopict)
    visitor = MyAritPlotVisitor(myg, debug)
    try:
        visitor.visit(tree)
    except UnknownIdentifier as exc:  # Visitor's exception
        print('Unknown identifier: {}'.format(exc.args[0]))
        exit(-1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AritPlot mini-project')
    parser.add_argument('filename', type=str,
                        help='Source file.')
    parser.add_argument('--nopict', action="store_false",
                        help='Do not open the Graphical Frame')
    args = parser.parse_args()
    main(args.filename, args.nopict)
