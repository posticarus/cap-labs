from APICodeLEIA import (
    DataLocation, Instru3A, Register,
    R0, R1, R2, R6, R7, Indirect
    )

# Allocation for Lab 5: the naive allocation is implemented
# The "all in mem" strategy is TODO.

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
    # TODO: compute before,after,args.
    i = Instru3A(ins, args=args)
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
