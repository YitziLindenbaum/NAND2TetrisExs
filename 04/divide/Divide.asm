// Divides two numbers
// The two numbers are found in RAM[13] and RAM[14] respectively
// The quotient is stored in RAM[15]
// The remainder of any division is ignored

// Algorithm:

// quotient = 0
// remainder = 0
// for i=n-1...0:
//     remainder = remainder <<
//     remainder[0] = RAM[13][i]
//     if remainder >= RAM[14]:
//         remainder = remainder - RAM[14]
//         quotient[i] = 1


@R15
M=0 // Init the quotient to 0
@remainder
M=0 // Init the remainder to 0

@15
D=A
@i
M=D  // Set i to 15 (the number of bits in RAM[13])

(LOOP)
    @i
    M=M-1 // i--
    D=M
    @END
    D; JLT

    @remainder
    M=M<<

    @counter
    M=1
    @R13
    D=M
    @shifted
    M=D // Store the value of RAM[13] in 'shifted'

    @i
    D=M
    @LOOP_CONT
    D; JEQ // Check to see if i=0

(SHIFT_R13_LOOP)
    @shifted
    M=M>> // Shift the value 'shifted' right by one bit

    @counter
    M=M+1 // counter++
    D=M
    @i
    D=M-D // D = i - counter
    @SHIFT_R13_LOOP
    D;JGE // If counter <= i, then continue to iterate in the loop

(LOOP_CONT)
    @1
    D=A
    @shifted
    D=M&D
    @remainder
    M=M|D // Set remainder[0] to RAM[13][i]

    @remainder
    D=M
    @R14
    D=D-M // D = remainder - RAM[14]
    @R15
    M=M<<
    @LOOP
    D; JLT // If remainder < RAM[14], then continue on to the next iteration of the loop

    @remainder
    M=D // remainder = remainder - RAM[14]
    @1
    D=A
    @R15
    M=M|D
    @LOOP
    0; JMP

(END)
