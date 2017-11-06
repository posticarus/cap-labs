#! /usr/bin/env python3
"""
Lab 6 Main File. Code Generation with Smart IRs.
Usage:
    python3 Main.py <filename>
"""
from MuLexer import MuLexer
from MuParser import MuParser
from MyMuCodeGen3AVisitor import MyMuCodeGen3AVisitor
from Allocations import smart_alloc
from ExpandJump import replace_jump

import argparse

from antlr4 import *
from sys import *
from os import *

from antlr4.tree.Trees import Trees

debug = True   # Should be False in your final version+make tests

def main(inputname, stdout=False, output_name=None):
    (hd, rest) = path.splitext(inputname)
    output_name = hd + ".s"
    print("Code will be generated in file " + output_name)

    input_s = FileStream(inputname)
    lexer = MuLexer(input_s)
    stream = CommonTokenStream(lexer)
    parser = MuParser(stream)
    tree = parser.prog()

    # Codegen 3@ CFG Visitor, first argument is debug mode
    visitor3 = MyMuCodeGen3AVisitor(debug, output_name, parser)

    visitor3.visit(tree)
    prog = visitor3.get_prog()

    exit(0)
    
    # prints the CFG as a dot file
    if debug:
        prog.printDot(hd+".dot")

    prog.printGenKill()

    mapin, mapout = prog.doDataflow()
    if debug:
        prog.printMapInOut()

    igraph = prog.doInterfGraph()

    if debug:
        print("printing the conflict graph")
        igraph.print_dot(hd+"_conflicts.dot")

    replace_jump(prog)  # replace conditional jump in the 3@code
    smart_alloc(prog, debug, hd+"_colored.dot")  # allocate
    prog.printCode(output_name, comment="Smart Allocation")
    visitor3.printRegisterMap()  # print decs.


# Now only smart allocation!

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate code for .mu file')
    parser.add_argument('filename', type=str,
                        help='Source file.')
    parser.add_argument('--stdout', action='store_true',
                        help='Generate code to stdout')
    parser.add_argument('--output', type=str,
                        help='Generate code to outfile')

    args = parser.parse_args()
    main(args.filename, args.stdout, args.output)
