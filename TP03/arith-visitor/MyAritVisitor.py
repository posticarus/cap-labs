from AritVisitor import AritVisitor
from AritParser import AritParser


class UnknownIdentifier(Exception):
    pass


class MyAritVisitor(AritVisitor):
    def __init__(self):
        self._memory = dict()  # store id -> values

    def visitNumberAtom(self, ctx):
        try:
            value = int(ctx.getText())
            return value
        except ValueError:
            return float(ctx.getText())

    def visitIdAtom(self, ctx):
        try:
            return self._memory[ctx.getText()]
        except KeyError:
            raise UnknownIdentifier(ctx.getText())

    def visitMultiplicationExpr(self, ctx):
        leftval = self.visit(ctx.expr(0))
        rightval = self.visit(ctx.expr(1))
        # an elegant way to match the token:
        if (ctx.mdop.type == AritParser.MULT):
            return leftval*rightval
        else:
            return leftval/rightval

    def visitAdditiveExpr(self, ctx):
        leftval = self.visit(ctx.expr(0))
        rightval = self.visit(ctx.expr(1))
        if (ctx.pmop.type == AritParser.PLUS):
            return leftval+rightval
        else:
            return leftval-rightval

    def visitExprInstr(self, ctx):
        val = self.visit(ctx.expr())
        print('The value is '+str(val))

    def visitParens(self, ctx):
        return self.visit(ctx.expr())

    def visitAssignInstr(self, ctx):
        val = self.visit(ctx.expr())
        name = ctx.ID().getText()
        print('now '+name+' has value '+str(val))
        self._memory[name] = val