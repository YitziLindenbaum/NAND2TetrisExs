// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

//while true:
//    if KBD != 0:
//        for addr in [SCREEN...SCREEN + 8191]:
//            RAM[addr] = -1 (1111... in binary)
//    else:
//        for addr in [SCREEN...SCREEN + 8191]:
//            RAM[addr] = 0 (0000... in binary)

(START)

    // save total number of words in screen in variable "last" - this will be
    // the number of iterations in our loops
    @8191
    D=A
    @last
    M=D

    // set variable addr to screen location
    @SCREEN
    D=A
    @addr
    M=D

    // set i (iterating variable) to 0
    @i
    M=0

    // check if any key is pressed (KBD != 0)
    @KBD
    D=M
    @WHITE
    D;JEQ // if KBD == 0, jump to white loop

    (BLACK)
        // if done with screen, go back to beginning of program
        @last
        D=M
        @i
        D=D-M
        @START
        D;JLT

        // set pixels to black
        @addr
        A=M
        M=-1 // R[addr] = 1111...

        @i
        M=M+1 // i++

        @addr
        M=M+1 // addr++

        @BLACK
        0;JMP // repeat loop

    (WHITE)
        // if done with screen, go back to beginning of program
        @last
        D=M
        @i
        D=D-M
        @START
        D;JLT

        // set pixels to white
        @addr
        A=M
        M=0 // R[addr] = 0000...

        @i
        M=M+1 // i++

        @addr
        M=M+1 // i++

        @WHITE
        0;JMP
