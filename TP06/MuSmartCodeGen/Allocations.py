from APICodeLEIA import (
    LEIAProg, DataLocation, Instru3A, Comment, Register,
    R0, R1, R2, R6, R7, Indirect
    )


def replace_reg(old_i):
    """Replace VirtualRegister operands with the corresponding allocated register."""
    ins, old_args = old_i.unfold()
    args = []
    for arg in old_args:
        if isinstance(arg, DataLocation) and arg.is_virtual():
            arg = arg.get_alloced_loc()
        args.append(arg)
    return [Instru3A(ins, args=args)]


def alloc_naive(src_prog):
    """Allocate all temporaries to registers. Fail if there are too many temporaries."""
    src_prog.naive_alloc()
    src_prog.iter_instructions(replace_reg)

    
def replace_mem(old_i):
    """Replace VirtualRegister operands with the corresponding allocated
    memory location. R6 points to the stack"""
    before = []
    after = []
    ins, old_args = old_i.unfold()
    args = []
    pos = 0
    numreg = 0
    for arg in old_args:
        if isinstance(arg, DataLocation) and arg.is_virtual():
            offset = arg.get_alloced_loc().get_offset()
            if pos == 0 and not old_i.is_read_only():
                # destination operand => add WMEM after
                after.append(Instru3A('SUB', R0, R6, offset))
                after.append(Instru3A('WMEM', R1, Indirect(R0)))
                arg = R1
            else:
                # source operand => add RMEM before
                numreg += 1
                before.append(Instru3A('SUB', R0, R6, offset))
                before.append(
                    Instru3A('RMEM', Register(numreg), Indirect(R0)))
                arg = Register(numreg)
        args.append(arg)
        pos += 1
    i = Instru3A(ins, args=args)
    return before + [i] + after


def replace_smart(old_i):
    before = []
    after = []
    ins, old_args = old_i.unfold()
    # print("coucou inside replace "+str(old_i))
    args = []
    pos = 0
    numreg = 0
    for arg in old_args:
        if isinstance(arg, DataLocation) and arg.is_virtual():
            arg = arg.get_alloced_loc()  # register or shift
            if not isinstance(arg, Register):
                offset = arg.get_offset()
                if pos == 0 and not old_i.is_read_only():
                    # destination operand => add WMEM after
                    after.append(Instru3A('SUB', R0, R6, offset))
                    after.append(Instru3A('WMEM', R1, Indirect(R0)))
                    arg = R1
                else:
                    # source operand => add RMEM before
                    numreg += 1
                    before.append(Instru3A('SUB', R0, R6, offset))
                    before.append(
                        Instru3A('RMEM', Register(numreg), Indirect(R0)))
                    arg = Register(numreg)
        args.append(arg)
        pos += 1
    # TODO RECHECK
    i = Instru3A(ins, args=args)  # change into args
    return before + [i] + after


def alloc_to_mem(src_prog):
    """Allocate all temporaries to memory.

    Hypothesis:

    - SNIF is never used right before an instruction that uses
    temporaries (otherwise we'd skip only the first instruction of the
    expanded instruction).

    - Expanded instructions can use r0 (to compute addresses), r1 and
    r2 (to store the values of temporaries before the actual
    instruction).
    """
    src_prog.alloc_to_mem()
    src_prog.iter_instructions(replace_mem)


def smart_alloc(src_prog, debug, name):
    """ Allocate all temporaries with graph coloring
    also prints the colored graph if debug
    """
    src_prog.smart_alloc(debug, name)
    src_prog.iter_instructions(replace_smart)
