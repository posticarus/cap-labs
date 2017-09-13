import sys

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener

from HelloLexer import HelloLexer
from HelloListener import HelloListener
from HelloParser import HelloParser

# cf https://stackoverflow.com/questions/32224980/python-2-7-antlr4-make-antlr-throw-exceptions-on-invalid-input # noqa


class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception("Syntax Error at line {}: {}".format(line, msg))

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex,
                        exact, ambigAlts, configs):
        raise Exception("Oh no!!")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex,
                                    stopIndex,
                                    conflictingAlts, configs):
        raise Exception("Oh no!!")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex,
                                 prediction, configs):
        raise Exception("Oh no!!")


class HelloPrintListener(HelloListener):  # this is a listener !
    def enterHi(self, ctx):
        print("Hello: {}".format(ctx.ID()))


def main():
    lexer = HelloLexer(InputStream(sys.stdin.read()))
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    parser._listeners = [MyErrorListener()]  # handling excep

    try:
        tree = parser.hi()
    except Exception as e:
        print(e)
        sys.exit(42)

    printer = HelloPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)


if __name__ == '__main__':
    main()
