#!/usr/bin/python3
# -*- coding: utf-8 -*-

from MuParser import MuParser
from LibGraphes import Graph

import sys
import networkx as nx
import graphviz as gz
import copy

# API for LEIA 3-address instructions
# + CFG construction + Dataflow Analysis.


# Utilitary function: pretty-prints a set of locations.
def regset_to_string(registerset):
    s = "{"+",".join(str(x) for x in registerset)+"}"
    return s


# Interfere function: True if t1 and t2 are in conflit.
def interfere(t1, t2, mapout, defined):
    return True # TODO !

class AllocationError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


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


class RegisterBase(DataLocation):
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
        # print("searching for "+str(reg))
        res = self._allocation[reg]
        return res

    def naive_alloc(self):
        """Performs a naive allocation: temp_0 -> r0, temp_1 -> r1, ..."""
        if len(self._registers) > 7:
            raise AllocationError("Cannot perform naive allocation with "
                                  "more than 8 temp ({})."
                                  .format(len(self._registers)))
        dict = {}
        n = 1  # Keep r0 for local temporary in code generation
        for vreg in self._registers:
            dict[vreg] = Register(n)
            n += 1
        self.set_reg_allocation(dict)

    def alloc_to_mem(self):
        """Performs the 'all to memory' allocation temp_i -> new place in
        memory. Does not use any register directly, but assumes R6
        points to the start of stack."""
        dict = {}
        n = 1
        for vreg in self._registers:
            dict[vreg] = Offset(Register(6), n)
            n += 1
        self.set_reg_allocation(dict)


    def smart_alloc(self, coloringreg, coloringspill):
        """Performs an allocation according to the graph coloring algorithm."""
        dict = {}
        # TODO!
        self.set_reg_allocation(dict)


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
        """Helper to traverse the CFG. Return true if self should be visited now.

        More precisely, return False if self has already been visited,
        or if self has a predecessor that has not been visited (in
        which case we will visit self later when all its precedessors
        will have been visited). Return True otherwise.
        """
        if self in visited:
            return False
        if self._in:
            for b in self._in:
                if b not in visited and b._i < self._i:
                    return False
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

    def printDot(self, graph, visited):
        """Prints the current block and its sons."""
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

    def printGenKill(self):
        print("pc = " + str(self._i))
        print("gen: " + regset_to_string(self._gen))
        print("kill: " + regset_to_string(self._kill) + "\n")

        # DATAFLOW PROPAGATION for one node. 
# propagate dataflow information: update _gen and _kill sets (mapin,mapout)
        # and make a recursive call to it sons.
    def do_dataflow_onestep(self, mapin, mapout, visited):
        """propagate dataflow information: update _gen and _kill sets
        (mapin,mapout) and make a recursive call to it sons.
        """
        if self.checkDep(visited):
            visited.add(self)
            i = self._i
            mapout[i] = set()  # new emptyset
            for child in self._out:
                mapout[i] = mapout[i].union(mapin[child._i])
                # update my _gen set
            mapin[i] = (mapout[i].difference(self._kill)).union(self._gen)
            for child in self._out:
                child.do_dataflow_onestep(mapin, mapout, visited)
        else:
            pass

    def update_defmap(self, defmap, visited):
        """Construct the map of blocks-> defs (=kill)."""
        if self.checkDep(visited):
            visited.add(self)
            i = self._i
            defmap[i] = self._kill
            for child in self._out:
                child.update_defmap(defmap, visited)
        else:
            pass

# A regular LEIA 3-address instruction has <=3 args, but the compJUMP has 4.


class Instru3A(Instruction):
    def __init__(self, ins, arg1=None, arg2=None, arg3=None, args=None):
        super().__init__()
        self._ins = ins
        if args:
            self.args = args
        else:
            self.args = [arg for arg in (arg1, arg2, arg3) if arg is not None]
        args = self.args
        self._left = args[0]
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
        Instruction.count = 0  # deterministic numbering of instructions for reproducible tests.
        self._listIns = []
        self._alltemps = []  # temporaries
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
        nt = self._pool.new_register()
        self._alltemps.append(nt)
        return nt

    def printTempList(self):
        print(self._alltemps)

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

    # each instruction has its own "add in list" version
    def addLabel(self, s):
        return self.add_instruction(s)

    def addComment(self, s):
        self.add_instruction(Comment(s))

    def addInstructionPRINT(self, expr):
        ins = Instru3A("print", expr)
        if not(isinstance(expr, Immediate)):
            ins._gen.add(expr)
        self.add_instruction(ins)

    def addInstructionJUMP(self, label):
        assert isinstance(label, Label)
        i = Instru3A("jump", label)
        # TODO ADD GEN KILL INIT IF REQUIRED
        self.add_instruction(i, False)
        # add in list but do not link with the following node
        self.add_edge(i, label)
        return i

    def addInstructionCondJUMP(self, label, op1, c, op2):
        assert isinstance(label, Label)
        assert isinstance(c, Condition)
        assert isinstance(op1, DataLocation)
        assert isinstance(op2, DataLocation)
        ins = Instru3A("cond_jump", args=[label, op1, c, op2])
        # TODO ADD GEN KILL INIT IF REQUIRED
        self.add_instruction(ins)
        self.add_edge(ins, label)
        return ins

    def addInstructionADD(self, dr, sr1, sr2orimm7):
        ins = Instru3A("add", dr, sr1, sr2orimm7)
        # TODO ADD GEN KILL INIT IF REQUIRED
        self.add_instruction(ins)

    def addInstructionSUB(self, dr, sr1, sr2orimm7):
        ins = Instru3A("sub", dr, sr1, sr2orimm7)
        # TODO ADD GEN KILL INIT IF REQUIRED
        self.add_instruction(ins)

    def addInstructionAND(self, dr, sr1, sr2orimm7):
        ins = Instru3A("and", dr, sr1, sr2orimm7)
        # TODO ADD GEN KILL INIT IF REQUIRED
        self.add_instruction(ins)

    def addInstructionOR(self, dr, sr1, sr2orimm7):
        ins = Instru3A("or", dr, sr1, sr2orimm7)
        # TODO ADD GEN KILL INIT IF REQUIRED
        self.add_instruction(ins)

    def addInstructionLET(self, dr, imm7):
        ins = Instru3A(".let", dr, imm7)
        # TODO ADD GEN KILL INIT IF REQUIRED
        self.add_instruction(ins)

    def addInstructionLETL(self, dr, imm7):
        ins = Instru3A("letl", dr, imm7)
        # TODO ADD GEN KILL INIT IF REQUIRED
        self.add_instruction(ins)

    def addInstructionCOPY(self, dr, sr):
        ins = Instru3A("copy", dr, sr)
        # TODO ADD GEN KILL INIT IF REQUIRED
        self.add_instruction(ins)

    def addInstructionRMEM(self, dr, sr):
        if isinstance(sr, RegisterBase):
            # Accept plain register where we expect an indirect
            # addressing mode.
            sr = Indirect(sr)
        ins = Instru3A("rmem", dr, sr)
        # TODO ADD GEN KILL INIT IF REQUIRED
        self.add_instruction(ins)

    def addInstructionWMEM(self, dr, sr):
        if isinstance(sr, RegisterBase):
            # Accept plain register where we expect an indirect
            # addressing mode.
            sr = Indirect(sr)
        ins = Instru3A("wmem", dr, sr)
        # TODO ADD GEN KILL INIT IF REQUIRED
        self.add_instruction(ins)

    # Allocation functions
    def naive_alloc(self):
        self._pool.naive_alloc()

    def alloc_to_mem(self):
        self._pool.alloc_to_mem()

    def smart_alloc(self, debug, outputname):
        if not self._igraph:
            print("hum, the interference graph seems to be empty")
            exit(1)
        # TODO :  color the graph with appropriate nb of colors,
        # and get back the (partial) coloring (see Libgraphes.py)
        # Then, make a call to self._pool.smart_alloc(coloring, ...)

    def printGenKill(self):
        print("Dataflow Analysis, Initialisation")
        i = 0
        while i < len(self._listIns):
            self._listIns[i].printGenKill()
            i += 1

    def printMapInOut(self):  # Prints in/out sets, useful for debug!
        print("In: {"+", ".join(str(x)+": "+regset_to_string(self._mapin[x])
                                for x in self._mapin.keys())+"}")
        print("Out: {"+", ".join(str(x)+": "+regset_to_string(self._mapout[x])
                                 for x in self._mapout.keys())+"}")

    # do Dataflow
    def doDataflow(self):
        print("Dataflow Analysis")
        countit = 0
        # initialisation of all mapout,mapin sets, and def = kill
        for i in range(len(self._listIns)):
            self._mapin[i] = set()
            self._mapout[i] = set()
        stable = False
        while not stable:
            stable = True # CHANGE
        # TODO ! (perform iterations until fixpoint).
        return(self._mapin, self._mapout)

    def doInterfGraph(self):
        self._start.update_defmap(self._mapdef, set())
        self._igraph = Graph()
        # self.printTempList()
        if not self._mapout and not self._mapin:
            print("hum, dataflow sets need to be initialised")
            exit(1)
        else:
            t = self._alltemps
            # TODO !
        return(self._igraph)

    # Dump code
    def printCode(self, filename, comment=None):
        """dump generated code on stdout or file."""
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
