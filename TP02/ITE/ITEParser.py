# Generated from ITE.g4 by ANTLR 4.7
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\6")
        buf.write("\26\4\2\t\2\4\3\t\3\4\4\t\4\3\2\3\2\3\3\3\3\5\3\r\n\3")
        buf.write("\3\4\3\4\3\4\3\4\3\4\5\4\24\n\4\3\4\2\2\5\2\4\6\2\2\2")
        buf.write("\24\2\b\3\2\2\2\4\f\3\2\2\2\6\16\3\2\2\2\b\t\5\4\3\2\t")
        buf.write("\3\3\2\2\2\n\r\5\6\4\2\13\r\7\5\2\2\f\n\3\2\2\2\f\13\3")
        buf.write("\2\2\2\r\5\3\2\2\2\16\17\7\3\2\2\17\20\7\5\2\2\20\23\5")
        buf.write("\4\3\2\21\22\7\4\2\2\22\24\5\4\3\2\23\21\3\2\2\2\23\24")
        buf.write("\3\2\2\2\24\7\3\2\2\2\4\f\23")
        return buf.getvalue()


class ITEParser ( Parser ):

    grammarFileName = "ITE.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'else'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "ID", "WS" ]

    RULE_prog = 0
    RULE_stmt = 1
    RULE_ifStmt = 2

    ruleNames =  [ "prog", "stmt", "ifStmt" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    ID=3
    WS=4

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ProgContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stmt(self):
            return self.getTypedRuleContext(ITEParser.StmtContext,0)


        def getRuleIndex(self):
            return ITEParser.RULE_prog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProg" ):
                listener.enterProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProg" ):
                listener.exitProg(self)




    def prog(self):

        localctx = ITEParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 6
            self.stmt()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StmtContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ifStmt(self):
            return self.getTypedRuleContext(ITEParser.IfStmtContext,0)


        def ID(self):
            return self.getToken(ITEParser.ID, 0)

        def getRuleIndex(self):
            return ITEParser.RULE_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStmt" ):
                listener.enterStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStmt" ):
                listener.exitStmt(self)




    def stmt(self):

        localctx = ITEParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stmt)
        try:
            self.state = 10
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ITEParser.T__0]:
                self.enterOuterAlt(localctx, 1)
                self.state = 8
                self.ifStmt()
                pass
            elif token in [ITEParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 9
                self.match(ITEParser.ID)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class IfStmtContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(ITEParser.ID, 0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ITEParser.StmtContext)
            else:
                return self.getTypedRuleContext(ITEParser.StmtContext,i)


        def getRuleIndex(self):
            return ITEParser.RULE_ifStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStmt" ):
                listener.enterIfStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStmt" ):
                listener.exitIfStmt(self)




    def ifStmt(self):

        localctx = ITEParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_ifStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.match(ITEParser.T__0)
            self.state = 13
            self.match(ITEParser.ID)
            self.state = 14
            self.stmt()
            self.state = 17
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.state = 15
                self.match(ITEParser.T__1)
                self.state = 16
                self.stmt()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





