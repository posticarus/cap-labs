from MuVisitor import MuVisitor
from MuParser import MuParser

from APICodeLEIA import (
    LEIAProg,
    Condition, Immediate,
    R7
    )

from antlr4.tree.Trees import Trees

class MyMuCodeGen3AVisitor(MuVisitor):

    def __init__(self, d, s, parser):
        super().__init__()
        self._outputname = s
        self._parser = parser
        self._debug = d
        self._memory = dict()
        # 3-address code generation
        self._prog = LEIAProg()
        self._lastlabel = ""
        self.ctx_stack = []

    def get_prog(self):
        return self._prog

    def printRegisterMap(self):
        print("--variables to memory map--")
        for keys, values in self._memory.items():
            print(keys + '-->' + str(values))

    # handle variable decl

    def visitVarDecl(self, ctx):
        vars_l = self.visit(ctx.id_l())
        for name in vars_l:
            if name in self._memory:
                print("Warning, variable %s has already been declared", name)
            else:
                self._memory[name] = self._prog.newtmp()
        return

    def visitIdList(self, ctx):
        t = self.visit(ctx.id_l())
        t.append(ctx.ID().getText())
        return t

    def visitIdListBase(self, ctx):
        return [ctx.ID().getText()]

    # expressions

    def visitParExpr(self, ctx):
        return self.visit(ctx.expr())

    def visitNumberAtom(self, ctx):
        s = ctx.getText()
        try:
            val = int(s)
            # this is valid for val beetween -2^15 and 2^15 -1
            dr = self._prog.newtmp()
            self._prog.addInstructionLET(dr, val)
            return dr
        except ValueError:
            raise Exception("Not Yet Implemented (float value)")

    def visitBooleanAtom(self, ctx):
        # true is 1 false is 0
        b = ctx.getText()
        dr = self._prog.newtmp()
        if b == 'true':
            val = 1
        else:
            val = 0
        self._prog.addInstructionLETL(dr, val)
        return dr

    def visitIdAtom(self, ctx):
        try:
            # get the register or the shift(dec) associated to id
            regval = self._memory[ctx.getText()]
            return regval
        except:
            # Should not happen (undeclared variables caught by
            # typing).
            raise

    def visitStringAtom(self, ctx):
        raise Exception("Not Yet Implemented (string atom)")

    def visitNilAtom(self, ctx):
        raise Exception("Not Yet Implemented (nil atom)")

    # now visit expr

    def visitAtomExpr(self, ctx):
        return self.visit(ctx.atom())

    def visitAdditiveExpr(self, ctx):
        tmpl = self.visit(ctx.expr(0))
        tmpr = self.visit(ctx.expr(1))
        dr = self._prog.newtmp()
        if ctx.myop.type == MuParser.PLUS:
            self._prog.addInstructionADD(dr, tmpl, tmpr)
        else:
            self._prog.addInstructionSUB(dr, tmpl, tmpr)
        return dr

    def visitOrExpr(self, ctx):
        tmpl = self.visit(ctx.expr(0))
        tmpr = self.visit(ctx.expr(1))
        dr = self._prog.newtmp()
        self._prog.addInstructionOR(dr, tmpl, tmpr)
        return dr

    def visitAndExpr(self, ctx):
        tmpl = self.visit(ctx.expr(0))
        tmpr = self.visit(ctx.expr(1))
        dr = self._prog.newtmp()
        self._prog.addInstructionAND(dr, tmpl, tmpr)
        return dr

    def visitEqualityExpr(self, ctx):
        return self.visitRelationalExpr(ctx)

    def visitRelationalExpr(self, ctx):
        if self._debug:
            print("relational expression:")
            print(Trees.toStringTree(ctx, None, self._parser))
        tmpl = self.visit(ctx.expr(0))
        tmpr = self.visit(ctx.expr(1))
        c = Condition(ctx.myop.type)
        dest = self._prog.newtmp()
        end_relational = self._prog.new_label('end_relational')
        self._prog.addInstructionLET(dest, 0)
        srctest = self._prog.addInstructionCondJUMP(end_relational,
                                                    tmpl, c.negate(),
                                                    tmpr)
        self._prog.addInstructionLET(dest, 1)
        desttest = self._prog.addLabel(end_relational)
        self._prog.add_edge(srctest, desttest)
        return dest

    def visitMultiplicativeExpr(self, ctx):
        raise Exception("Not Yet Implemented (multexpr)")

    def visitNotExpr(self, ctx):
        reg = self.visit(ctx.expr())
        dr = self._prog.newtmp()
        # there is no NOT instruction :-(
        labelneg, labelend = self._prog.newlabelCond()
        srccond = self._prog.addInstructionCondJUMP(labelneg, reg,
                                                    Condition("neq"),
                                                    Immediate(1))
        self._prog.addInstructionLETL(dr, 0)
        srcjump = self._prog.addInstructionJUMP(labelend)
        destcond = self._prog.addLabel(labelneg)
        self._prog.add_edge(srccond, destcond)
        self._prog.addInstructionLETL(dr, 1)
        destjump = self._prog.addLabel(labelend)
        self._prog.add_edge(srcjump, destjump)
        return dr

    def visitUnaryMinusExpr(self, ctx):
        raise Exception("Not Yet Implemented (unaryminusexpr)")

    def visitPowEpr(self, ctx):
        raise Exception("Not Yet Implemented (powexpr)")

    # statements

    def visitProgRule(self, ctx):
        self.visit(ctx.vardecl_l())
        self.visit(ctx.block())
        self.printRegisterMap()

    def visitAssignStat(self, ctx):
        if self._debug:
            print("assign statement, rightexpression is:")
            print(Trees.toStringTree(ctx.expr(), None, self._parser))
        reg4expr = self.visit(ctx.expr())
        name = ctx.ID().getText()
        # find in table
        if name in self._memory:
            self._prog.addInstructionCOPY(self._memory[name], reg4expr)
        else:
            raise Exception("Variable is not declared")

    def visitCondBlock(self, ctx):
        if self._debug:
            print("condblockstatement, condition is:")
            print(Trees.toStringTree(ctx.expr(), None, self._parser))
            print("and block is:")
            print(Trees.toStringTree(ctx.stat_block(), None, self._parser))
        end_if = self.ctx_stack[-1]
        next_cond = self._prog.new_label('end_cond')
        cond = self.visit(ctx.expr())
        src_cond = self._prog.addInstructionCondJUMP(next_cond, cond,
                                                     Condition('eq'), Immediate(0))
        self.visit(ctx.stat_block())
        i = self._prog.addInstructionJUMP(end_if)
        self._prog.addLabel(next_cond)
        return src_cond

    def visitIfStat(self, ctx):
        if self._debug:
            print("if statement")
        if_ctxendif = self._prog.new_label("end_if")
        self.ctx_stack.append(if_ctxendif)
        for cb in ctx.condition_block():
            jumpsrc = self.visit(cb)
        if ctx.stat_block() is not None:
            if self._debug:
                print("else  ")
            self.visit(ctx.stat_block())  # else branch code
        # NOP, to avoid jump with offset +1.
        self._prog.addInstructionSUB(R7, R7, Immediate(0))
        self._prog.addLabel(if_ctxendif)
        self.ctx_stack.pop()

    def visitWhileStat(self, ctx):
        if self._debug:
            print("while statement, condition is:")
            print(Trees.toStringTree(ctx.expr(), None, self._parser))
            print("and block is:")
            print(Trees.toStringTree(ctx.stat_block(), None, self._parser))
        # TODO

    def visitLogStat(self, ctx):
        expr_loc = self.visit(ctx.expr())
        if self._debug:
            print("log statement, expression is:")
            print(Trees.toStringTree(ctx.expr(), None, self._parser))
        self._prog.addInstructionPRINT(expr_loc)

    def visitStatList(self, ctx):
        for stat in ctx.stat():
            self._prog.addComment(Trees.toStringTree(stat, None, self._parser))
            self.visit(stat)
