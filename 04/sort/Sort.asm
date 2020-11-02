// Sorts an array in descending order.
// The array can be found at the address stored in RAM[14]
// The length of the array is found in RAM[15]

// Algorithm

// for i=RAM[15]-1...1:
//     for j=0...i-1:
//         if RAM[14] + j < RAM[14] + j + 1:
//             flip(RAM[14] + j, RAM[14] + j + 1)


(INIT_OUTER_LOOP)
    @R15
    D=M-1
    @END
    D; JLE // Check that the array has more than one element; otherwise, no sorting is necessary

    @i
    M=D+1 // Set i=RAM[15]

(OUTER_LOOP)
    @i
    M=M-1 // M--
    D=M-1
    @END
    D; JLE // Check that i >= 2

(INIT_INNER_LOOP)
    @j
    M=-1 // Set j=0

(INNER_LOOP)
    @j
    M=M+1 // j++
    D=M
    @i
    D=M-D // D = i - j
    D=D-1
    @OUTER_LOOP
    D; JLT // If j > i-1, then exit the inner loop and return to the outer loop

    @j
    D=M
    @R14
    D=D+M
    @left
    M=D // left=R14+j

    @j
    D=M+1
    @R14
    D=D+M
    @right
    M=D // right=R14+j+1

    @left
    A=M
    D=M
    @right
    A=M
    D=D-M // D = (R14+j) - (R14+j+1)

    @FLIP
    D; JLT // Jump if R14+j is less than R14+j+1
    @INNER_LOOP
    0; JMP // Otherwise, continue to the next iteration of the inner loop

(FLIP)
// Assumes that the addresses to the two numbers
// to be flipped are stored in @left and @right, respectively
    @left
    A=M
    D=M
    @temp
    M=D // temp = RAM[left]

    @right
    A=M
    D=M
    @left
    A=M
    M=D // RAM[left] = RAM[right]

    @temp
    D=M
    @right
    A=M
    M=D // RAM[right] = temp

    @INNER_LOOP
    0; JMP

(END)
