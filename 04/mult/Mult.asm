// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Algorithm:

// if R1 > R0:
//    switch(R1, R0)

// R2 = 0
// for i in range(R1):
//    R2 += R0

// Check R0 >= R1
@R1
D=M
@R0
D=D-M
@INIT_LOOP
D;JLE

// flip(R1, R0)
@R1
D=M
@temp
M=D // temp = R1

@R0
D=M
@R1
M=D //  R1 = R0

@temp
D=M
@R0
M=D  //  R0 = temp

(INIT_LOOP)
    @R2
    M=0 // Init R2 to 0
    @R1
    D=M
    @END
    D;JEQ // If R1 == 0: Skip to end; product will be zero
    @counter
    M=1 // Init counter to 1

(LOOP)
    @R0
    D=M
    @R2
    M=M+D // R2 += R0

    @counter
    M=M+1 // counter++
    D=M
    @R1
    D=M-D
    @LOOP
    D;JGE // if counter <= R1, iterate again




