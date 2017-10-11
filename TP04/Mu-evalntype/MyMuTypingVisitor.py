from MuVisitor import MuVisitor
from MuParser import MuParser

from enum import Enum


class MuTypeError(Exception):
    pass


class BaseType(Enum):
    Float, Integer, Boolean, String, Nil = range(5)

    def printBaseType(self):
        print(self)


# Basic Type Checking for Mu programs.
class MyMuTypingVisitor(MuVisitor):

    def __init__(self):
        self._memorytypes = dict()  # id-> types

    def _raise(self, ctx, for_what, *types):
        raise MuTypeError(
            'Line {} col {}: invalid type for {}: {}'.format(
                ctx.start.line, ctx.start.column, for_what,
                ' and '.join(t.name.lower() for t in types)))

    # type declaration

    def visitVarDecl(self, ctx):
        vars_l = self.visit(ctx.id_l())
        tt = self.visit(ctx.typee())
        for name in vars_l:
            self._memorytypes[name] = tt
        return

    def visitBasicType(self, ctx):
        if ctx.mytype.type == MuParser.INTTYPE:
            return BaseType.Integer
        elif ctx.mytype.type == MuParser.FLOATTYPE:
            return BaseType.Float
        elif ctx.mytype.type == MuParser.BOOLTYPE:
            return BaseType.Boolean
        elif ctx.mytype.type == MuParser.STRINGTYPE:
            return BaseType.String
        else:
            return BaseType.Nil

    def visitIdList(self, ctx):
        t = self.visit(ctx.id_l())
        t.append(ctx.ID().getText())
        return t

    def visitIdListBase(self, ctx):
        return [ctx.ID().getText()]

    # typing visitors for expressions, statements !

