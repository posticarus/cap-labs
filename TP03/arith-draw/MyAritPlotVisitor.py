from AritPlotVisitor import AritPlotVisitor
from AritPlotParser import AritPlotParser

from math import cos, sin, pi, floor


class UnknownIdentifier(Exception):
    pass


class MyAritPlotVisitor(AritPlotVisitor):

    def __init__(self, mypic, debug):
        self._memory = dict()  # store id -> values
        self._myg = mypic
        self._debug = debug

    def visitStatementList(self, ctx):  # method overriding in Python
        n = len(ctx.statement())
        if self._debug:
            print("Program with " + str(n) + " instructions.")
        for ins in ctx.statement():
            self.visit(ins)
        self._myg.showPicture()

    def visitPrintPlotInstr(self, ctx):
        pass
            
    def visitAssignInstr(self, ctx):
        val = self.visit(ctx.expr())
        name = ctx.ID().getText()
        if self._debug:
            print('now ' + name + ' has value ' + str(val))
        self._memory[name] = val

    def visitExprInstr(self, ctx):
        val = self.visit(ctx.expr())
        if self._debug:
            print('expr instr, value is ' + str(val))
        return val

    def visitQuitInstr(self, ctx):
        return 0  # trouver un truc

    # expressions

    def visitOppExpr(self, ctx):
        leftval = self.visit(ctx.expr())
        return (- leftval)

    def visitAdditiveExpr(self, ctx):
        leftval = self.visit(ctx.expr(0))
        rightval = self.visit(ctx.expr(1))
        if (ctx.pmop.type == AritPlotParser.PLUS):
            return leftval + rightval
        else:
            return leftval - rightval

    def visitMultiplicationExpr(self, ctx):
        leftval = self.visit(ctx.expr(0))
        rightval = self.visit(ctx.expr(1))
        if (ctx.mdop.type == AritPlotParser.MULT):
            return leftval * rightval
        else:
            return leftval / rightval

    def visitTrigoExpr(self, ctx):
        pass
        
    # atoms

    def visitParens(self, ctx):
        return self.visit(ctx.expr())

    def visitNumberAtom(self, ctx):
        try:
            value = int(ctx.getText())
            return value
        except ValueError:
            return float(ctx.getText())

    def visitPiAtom(self, ctx):
        pass

    def visitIdAtom(self, ctx):
        try:
            return self._memory[ctx.getText()]
        except KeyError:
            raise UnknownIdentifier(ctx.getText())
