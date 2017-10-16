#!/usr/bin/python3
# -*- coding: utf-8 -*-

from MuParser import MuParser

import sys
import networkx as nx
import graphviz as gz

# API for LEIA 3-address instructions (+CFG)
# You only have to modify the alloc_to_mem method


class AllocationError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class CodeGenContext():
    """In a normal recursive algorithm we would transmit the parameters
    (e.g. labels like end_if) to recursive calls on child nodes, but
    the visitor pattern does not allow that, so we deal with it with
    our own stack.

    This is a convenience class that allows writting code like

    class FooBarVisitor(..., CodeGenContextStack): # Multiple inheritence
                                                   # (mixins)

        def visitIfStat(...):
            if_ctx = CodeGenContext()  # Create context
                                           # and push it on stack
            if_ctx.end_label = ...  # fill-in the context with
                                    # what you want
            self.ctx_stack.append(if_ctx)
            ... self.visit(...) ...
            self.ctx_stack.pop()  # Remove the context from stack

        def visit...(...):
            ... = self.ctx_stack[-1].end_label  # Use the context created above.
    """



class Operand():
    pass


class Condition(Operand):
    """Condition, i.e. second operand of the SNIF instruction."""
    def __init__(self, optype):
        if isinstance(optype, str):
            op = optype
        elif optype == MuParser.GT:
            op = 'gt'
        elif optype == MuParser.GTEQ:
            op = 'ge'
        elif optype == MuParser.LT:
            op = 'lt'
        elif optype == MuParser.EQ:
            op = 'eq'
        elif optype == MuParser.NEQ:
            op = 'neq'
        elif optype == MuParser.LTEQ:
            op = 'le'
        else:
            raise Exception("Unsupported comparison operator" + optype)
        self._op = op

    def negate(self):
        if self._op == 'gt':
            return Condition('le')
        elif self._op == 'ge':
            return Condition('lt')
        elif self._op == 'lt':
            return Condition('ge')
        elif self._op == 'le':
            return Condition('gt')
        elif self._op == 'eq':
            return Condition('neq')
        elif self._op == 'neq':
            return Condition('eq')

    def __str__(self):
        return self._op


class DataLocation(Operand):
    def is_register(self):
        """True if the location is a register (virtual or real)."""
        return False

    def is_virtual(self):
        """True if the location is virtual, i.e. needs to be replaced during
        code generation."""
        return False


class Offset(DataLocation):
    def __init__(self, basereg, offset):
        super().__init__()
        assert isinstance(offset, int)
        self._offset = offset
        self._basereg = basereg

    def __str__(self):
        return "offset " + str(self._offset) + " from " + str(self._basereg)

    def get_offset(self):
        return self._offset

    def to_reg(self, prog, reg):
        """Generate code to load the value in register 'reg'.

        Not used in the current version of code generation (TODO: remove?)."""
        prog.addInstructionSUB(R0, self._basereg, self._offset)
        prog.addInstructionRMEM(reg, R0)

    def store_from_reg(self, prog, reg):
        """Generate code to store the value of 'reg' in this location.

        Not used in the current version of code generation (TODO: remove?)."""
        prog.addInstructionSUB(R0, self._basereg, self._offset)
        prog.addInstructionWMEM(reg, R0)


class RegisterBase(DataLocation):
    def to_reg(self, prog, reg):
        """Generate code to load the value in register 'reg'.

        Not used in the current version of code generation (TODO: remove?)."""
        prog.addInstructionCOPY(reg, self)

    def store_from_reg(self, prog, reg):
        """Generate code to store the value of 'reg' in this location.

        Not used in the current version of code generation (TODO: remove?)."""
        prog.addInstructionCOPY(self, R0)

    def is_register(self):
        return True


class Register(RegisterBase):
    def __init__(self, number):
        super().__init__()
        self._number = number

    def __str__(self):
        return 'r' + str(self._number)


class Indirect(DataLocation):
    """Operand of the form [reg], designating the memory location pointed
    to by reg."""
    def __init__(self, reg):
        super().__init__()
        self._reg = reg

    def __str__(self):
        return '[' + str(self._reg) + ']'


class Immediate(DataLocation):
    """Immediate operand (integer)."""
    def __init__(self, val):
        super().__init__()
        self._val = val

    def __str__(self):
        return str(self._val)


# Shortcuts for registers
R0 = Register(0)
R1 = Register(1)
R2 = Register(2)
R3 = Register(3)
R4 = Register(4)
R5 = Register(5)
R6 = Register(6)
R7 = Register(7)


class VirtualRegisterPool:
    """Manage a pool of virtual registers."""
    def __init__(self):
        self._registers = set()
        self._allocation = None
        self._current_num = 0

    def is_allocated(self):
        """True if set_reg_allocation() has already been called on this
        pool."""
        return self._allocation is not None

    def add_register(self, reg):
        """Add a register to the pool."""
        self._registers.add(reg)

    def set_reg_allocation(self, allocation):
        """Give a mapping from virtual registers to actual registers.

        allocation must be a dict from VirtualRegister to Register.
        """
        self._allocation = allocation

    def new_register(self):
        r = VirtualRegister(self._current_num, self)
        self.add_register(r)
        self._current_num += 1
        return r

    def get_alloced_loc(self, reg):
        """Get the actual register allocated for the virtual register reg."""
        return self._allocation[reg]

    def naive_alloc(self):
        """Perform a naive allocation: temp_0 -> r0, temp_1 -> r1, ..."""
        if len(self._registers) > 7:
            raise AllocationError("Cannot perform naive allocation with "
                                  "more than 7 temp ({})."
                                  .format(len(self._registers)))
        dict = {}
        n = 1  # Keep r0 for local temporary in code generation
        for vreg in self._registers:
            dict[vreg] = Register(n)
            n += 1
        self.set_reg_allocation(dict)

    def alloc_to_mem(self):
        """Performs the all to memory allocation temp_i -> new place in
        memory, also keep r0 for local temporary in code generation """
        pass # TODO !


class VirtualRegister(RegisterBase):
    """Virtual register, aka "temporaries" are locations that haven't been
    allocated yet. They will later be mapped to physical registers
    (Register) or to a memory location."""
    def __init__(self, number, pool):
        self._number = number
        self._pool = pool
        pool.add_register(self)

    def __str__(self):
        return 'temp_' + str(self._number)

    def get_alloced_loc(self):
        return self._pool.get_alloced_loc(self)

    def is_virtual(self):
        return True


class Instruction:
    """Real instruction, comment or label."""
    count = 0

    def __init__(self):
        self._i = Instruction.count
        self._isnotStart = True
        self._in = []
        self._out = []
        self._MAXOUT = 1  # Most blocks can have only one successor
        self._ins = None
        self._left = None
        self._right = None
        Instruction.count += 1
        # for liveness dataflow analysis (Lab 6)
        self._gen = set()  # should be initialised somewhere
        self._kill = set()

    def is_instruction(self):
        """True if the object is a true instruction (not a label or
        comment)."""
        return False

    def checkDep(self, visited):
        if self in visited:
            return False
        if self._in:
            for b in self._in:
                if b not in visited and b._i < self._i:
                    return False
            return True
        else:
            return True

    def printIns(self, stream, visited, alloc):
        if self.checkDep(visited):
            visited.add(self)
            if self._ins:
                self._ins.printIns(stream, alloc)
            if self._out:
                # print("nb of childs="+str(len(self._out)))
                for child in self._out:
                    child.printIns(stream, visited, alloc)
        else:
            pass

        # Prints the current block and its sons.
    def printDot(self, graph, visited):
        if self.checkDep(visited):
            visited.add(self)
            if self._isnotStart:
                    s1 = str(self._i) + "_" + str(self)
            else:
                s1 = "START"
            graph.add_node(s1)
            if self._out:
                for child in self._out:
                    s2 = str(child._i) + "_" + str(child)
                    graph.add_edge(s1, s2)
                    child.printDot(graph, visited)
        else:
            pass

# A regular LEIA 3-adress instruction has <=3 args, but the compJUMP has 4.


class Instru3A(Instruction):
    def __init__(self, ins, arg1=None, arg2=None, arg3=None, args=None):
        super().__init__()
        self._ins = ins
        if args:
            self.args = args
        else:
            self.args = [arg for arg in (arg1, arg2, arg3) if arg is not None]
        args = self.args
        self._left = arg1
        if len(self.args) >= 3:
            self._right = (self.args[1], self.args[2])
        elif len(self.args) >= 2:
            self._right = (self.args[1],)
        for i in range(len(args)):
            if isinstance(args[i], int):
                args[i] = Immediate(args[i])
            assert isinstance(args[i], Operand), (args[i], type(args[i]))

    def is_instruction(self):
        """True if the object is a true instruction (not a label or
        comment)."""
        return True

    def get_name(self):
        return self._ins.upper()

    def is_read_only(self):
        """True if the instruction only reads from its operands.

        Otherwise, the first operand is considered as the destination
        and others are source.
        """
        return (self.get_name() == 'PRINT' or
                self.get_name() == 'SNIF')

    def __str__(self):
        s = self._ins
        for arg in self.args:
            s += ' ' + str(arg)
        return s

    def printIns(self, stream):
        """Print the instruction on the output."""
        print('       ', str(self), file=stream)

    def unfold(self):
        """Utility function to get both the instruction name and the operands
        in one call. Example:

        ins, args = i.unfold()
        """
        return self.get_name(), self.args


class Label(Instruction, Operand):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name

    def __str__(self):
        return "lbl_"+self._name

    def printIns(self, stream):
        print(str(self) + ':', file=stream)


class Comment(Instruction):
    def __init__(self, content, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._content = content

    def __str__(self):  # use only for printDot !
        return "comment"

    def printIns(self, stream):
        print('        ;; ' + self._content, file=stream)


class LEIAProg:
    def __init__(self):
        self._listIns = []
        self._nbtmp = -1
        self._nblabel = -1
        self._dec = -1
        self._pool = VirtualRegisterPool()
        # CFG Stuff - Lab 6 Only
        self._start = None
        self._end = None
        self._mapin = {}  # will be map block -> set of variables
        self._mapout = {}
        self._mapdef = {}  # block : defined = killed vars in the block
        self._igraph = None  # interference graph

    def add_edge(self, src, dest):
        dest._in.append(src)
        src._out.append(dest)

    def add_instruction(self, i, linkwithsucc=True):
        """Utility function to add an instruction in the program.
        in Lab 5, only add at the end of the instruction list (_listIns)
        in Lab 6, will be used to also add in the CFG structure.
        """
        if not self._listIns:  # empty list: empty prg
            i._isnotStart = False
            self._start = i
            self._end = i
        else:
            if self._end is not None:
                self._end._out.append(i)
                i._in.append(self._end)
            self._end = i
            if not linkwithsucc:
                self._end = None
        self._listIns.append(i)
        return i

    def iter_instructions(self, f):

        """Iterate over instructions.

        For each real instruction (not label or comment), call f,
        which must return either None or a list of instruction. If it
        returns None, nothing happens. If it returns a list, then the
        instruction is replaced by this list.

        """
        i = 0
        while i < len(self._listIns):
            old_i = self._listIns[i]
            if not old_i.is_instruction():
                i += 1
                continue
            new_i_list = f(old_i)
            if new_i_list is None:
                i += 1
                continue
            del self._listIns[i]
            self._listIns.insert(i, Comment(str(old_i)))
            i += 1
            for new_i in new_i_list:
                self._listIns.insert(i, new_i)
                i += 1
            self._listIns.insert(i, Comment("end " + str(old_i)))
            i += 1

    def get_instructions(self):
        return self._listIns

    def new_location(self, three_addr):
        if three_addr:
            return self.newtmp()
        else:
            return self.new_offset()

    def newtmp(self):
        return self._pool.new_register()

    def new_offset(self):
        self._dec = self._dec + 1
        return Offset(R6, self._dec)

    def new_label(self, name):
        self._nblabel = self._nblabel + 1
        return Label(name + "_" + str(self._nblabel))

    def newlabelWhile(self):
        self._nblabel = self._nblabel + 1
        return (Label("l_while_begin_" + str(self._nblabel)),
                Label("l_while_end_" + str(self._nblabel)))

    def newlabelCond(self):
        self._nblabel = self._nblabel + 1
        return (Label("l_cond_neg_" + str(self._nblabel)),
                Label("l_cond_end_" + str(self._nblabel)))

    def newlabelIf(self):
        self._nblabel = self._nblabel + 1
        return (Label("l_if_false_" + str(self._nblabel)),
                Label("l_if_end_" + str(self._nblabel)))

    # each instruction has its own "add in list" version
    def addLabel(self, s):
        return self.add_instruction(s)

    def addComment(self, s):
        self.add_instruction(Comment(s))

    def addInstructionSNIF(self, left, op, right):
        self.add_instruction(Instru3A("snif", left, op, right))

    def addInstructionPRINT(self, expr):
        self.add_instruction(Instru3A("print", expr))

    def addInstructionJUMP(self, label):
        assert isinstance(label, Label)
        i = Instru3A("jump", label)
        self.add_instruction(i, False)
        # add in list but do not link with the following node
        self.add_edge(i, label)
        return i

    def addInstructionCondJUMP(self, label, op1, c, op2):
        assert isinstance(label, Label)
        assert isinstance(c, Condition)
        i = Instru3A("cond_jump", args=[label, op1, c, op2])
        self.add_instruction(i)
        self.add_edge(i, label)
        return i

    def addInstructionADD(self, dr, sr1, sr2orimm7):
        self.add_instruction(
            Instru3A("add", dr, sr1, sr2orimm7))

    def addInstructionSUB(self, dr, sr1, sr2orimm7):
        self.add_instruction(
            Instru3A("sub", dr, sr1, sr2orimm7))

    def addInstructionAND(self, dr, sr1, sr2orimm7):
        self.add_instruction(
            Instru3A("and", dr, sr1, sr2orimm7))

    def addInstructionLET(self, dr, imm7):
        self.add_instruction(Instru3A(".let", dr, imm7))

    def addInstructionLETL(self, dr, imm7):
        self.add_instruction(Instru3A("letl", dr, imm7))

    def addInstructionCOPY(self, dr, sr):
        self.add_instruction(Instru3A("copy", dr, sr))

    def addInstructionRMEM(self, dr, sr):
        if isinstance(sr, RegisterBase):
            # Accept plain register where we expect an indirect
            # addressing mode.
            sr = Indirect(sr)
        self.add_instruction(
            Instru3A("rmem", dr, sr))

    def addInstructionWMEM(self, dr, sr):
        if isinstance(sr, RegisterBase):
            # Accept plain register where we expect an indirect
            # addressing mode.
            sr = Indirect(sr)
        self.add_instruction(
            Instru3A("wmem", dr, sr))

    # Allocation functions
    def naive_alloc(self):
        self._pool.naive_alloc()

    def alloc_to_mem(self):
        self._pool.alloc_to_mem()

    # Dump code
    def printCode(self, filename, comment=None):
        # dump generated code on stdout or file.
        output = open(filename, 'w') if filename else sys.stdout
        print(';;Automatically generated LEIA code, 2017', file=output)
        if comment is not None:
            print(';; "' + comment + '" version', file=output)
        print(';stack management\n.set r6 stack\n', file=output)
        for i in self._listIns:
            i.printIns(output)
        print('\n\n;;postlude\njump 0', file=output)
        print('.align16', file=output)
        print('stackend:', file=output)
        print('.reserve 42', file=output)
        print('stack:', file=output)
        if output is not sys.stdout:
            output.close()

    def printDot(self, filename):
        # Only used in Lab 6
        graph = nx.DiGraph()
        self._start.printDot(graph, set())
        graph.graph['graph'] = dict()
        graph.graph['graph']['overlap'] = 'false'
        nx.drawing.nx_agraph.write_dot(graph, filename)
        gz.render('dot', 'pdf', filename)
        gz.view(filename + '.pdf')
