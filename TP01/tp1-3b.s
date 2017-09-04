    ;;  graphical "reserved" registers: r1,2,3,4
    ;;  r12 for the star
    call clearscr
    .let r4 1
    .let r0 0x0000
    .let r2 95
    .let r1 10
    .set r10 star           ; takes the @ - not affected
    .set r14 N
    rmem r6 [r14]           ; loop counter init=N
loopi:
    rmem r3 [r10]
    copy r13 r6
    copy r12 r2
    copy r11 r1
    call putchar            ; store the context before call
    refresh
    copy r1 r11
    copy r2 r12
    copy r6 r13
    add r1 r1 15
    sub r6 r6 1
    snif r6 eq 0
    jump loopi
    jump 0

star:
    .word 42                ; ascii for '*'
N:
    .word 4


#include lib.s

