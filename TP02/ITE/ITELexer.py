# Generated from ITE.g4 by ANTLR 4.7
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\6")
        buf.write("\37\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\3\2\3\2\3\2\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\4\6\4\25\n\4\r\4\16\4\26\3\5\6\5")
        buf.write("\32\n\5\r\5\16\5\33\3\5\3\5\2\2\6\3\3\5\4\7\5\t\6\3\2")
        buf.write("\4\4\2C\\c|\5\2\13\f\17\17\"\"\2 \2\3\3\2\2\2\2\5\3\2")
        buf.write("\2\2\2\7\3\2\2\2\2\t\3\2\2\2\3\13\3\2\2\2\5\16\3\2\2\2")
        buf.write("\7\24\3\2\2\2\t\31\3\2\2\2\13\f\7k\2\2\f\r\7h\2\2\r\4")
        buf.write("\3\2\2\2\16\17\7g\2\2\17\20\7n\2\2\20\21\7u\2\2\21\22")
        buf.write("\7g\2\2\22\6\3\2\2\2\23\25\t\2\2\2\24\23\3\2\2\2\25\26")
        buf.write("\3\2\2\2\26\24\3\2\2\2\26\27\3\2\2\2\27\b\3\2\2\2\30\32")
        buf.write("\t\3\2\2\31\30\3\2\2\2\32\33\3\2\2\2\33\31\3\2\2\2\33")
        buf.write("\34\3\2\2\2\34\35\3\2\2\2\35\36\b\5\2\2\36\n\3\2\2\2\5")
        buf.write("\2\26\33\3\b\2\2")
        return buf.getvalue()


class ITELexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    ID = 3
    WS = 4

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'if'", "'else'" ]

    symbolicNames = [ "<INVALID>",
            "ID", "WS" ]

    ruleNames = [ "T__0", "T__1", "ID", "WS" ]

    grammarFileName = "ITE.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


