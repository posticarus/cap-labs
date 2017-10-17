from APICodeLEIA import Instru3A

# This is only done to rewrite conditional jumps into snif
# This file should not be modified.


def replace_jump_i(old_i):
    """Replace CondJUMP instructions with SNIF+JUMP."""
    ins, args = old_i.unfold()
    if ins != 'COND_JUMP':
        return
    target_label, op1, c, op2 = args
    return [
        Instru3A('SNIF', op1, c.negate(), op2),
        Instru3A('JUMP', target_label),
    ]


def replace_jump(src_prog):
    src_prog.iter_instructions(replace_jump_i)
