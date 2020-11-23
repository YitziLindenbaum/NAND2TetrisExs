ACCESS_STACK = "@SP\nA=M-1\n"  # Sets A-reg at top of stack
DECREASE_STACK_PTR = "@SP\nM=M-1\n"

EQ_CODE = "D=M-D\n@TRUE_{counter}\nD;JEQ\n@SP\nA=M-1\nA=A-1\nM=0\n" \
          "@END_TRUE_{counter}\n0;JMP\n(TRUE_{counter})\n" \
          "@SP\nA=M-1\nA=A-1\nM=-1\n(END_TRUE_{counter})\n"

LT_CODE = "D=M\n@y\nM=D\n@SP\nA=M-1\nA=A-1\nD=M\n@x\nM=D\n" \
          "@X_NEG_{counter}\nD;JLT\n@y\nD=M\n@FALSE_{counter}\nD;JLE\n" \
          "@SAME_SGN_{counter}\n0;JMP\n(X_NEG_{counter})\n@y\nD=M\n@TRUE_{" \
          "counter}\nD;JGE\n(SAME_SGN_{counter})\n@x\nD=M-D\n@TRUE_{" \
          "counter}\nD;JLT\n(FALSE_{counter})\n@SP\nA=M-1\nA=A-1\nM=0\n" \
          "@END_{counter}\n0;JMP\n(TRUE_{counter})\n@SP\nA=M-1\nA=A-1\n" \
          "M=-1\n(END_{counter})\n"

GT_CODE = "D=M\n@y\nM=D\n@SP\nA=M-1\nA=A-1\nD=M\n@x\nM=D\n" \
          "@X_POS_{counter}\nD;JGT\n@y\nD=M\n@FALSE_{counter}\nD;JGE\n" \
          "@SAME_SGN_{counter}\n0;JMP\n(X_POS_{counter})\n@y\nD=M\n@TRUE_{" \
          "counter}\nD;JLE\n(SAME_SGN_{counter})\n@x\nD=M-D\n@TRUE_{" \
          "counter}\nD;JGT\n(FALSE_{counter})\n@SP\nA=M-1\nA=A-1\nM=0\n" \
          "@END_{counter}\n0;JMP\n(TRUE_{counter})\n@SP\nA=M-1\nA=A-1\n" \
          "M=-1\n(END_{counter})\n"


class CodeWriter:

    def __init__(self, file):
        """
        :param file: An already opened Assembly file to write to
        """
        self.asm_file = file
        self.vm_file = None
        self.static_ptr = 0
        self.counter = 0

    def set_file_name(self, file_name: str):
        """
        Informs the code writer that the translation of the new VM file has started
        """
        self.vm_file = file_name

    def write_arithmetic(self, command: str):
        """
        Writes the assembly code that is the translation of the given command.
        """
        self.asm_file.write(ACCESS_STACK)

        # < and > -- special treatment
        if command == "gt":
            self.asm_file.write(GT_CODE.format(counter=self.counter))
            self.counter += 1
            self.asm_file.write(DECREASE_STACK_PTR)
        elif command == "lt":
            self.asm_file.write(LT_CODE.format(counter=self.counter))
            self.counter += 1
            self.asm_file.write(DECREASE_STACK_PTR)

        # Unitary commands
        elif command == "neg":
            self.asm_file.write("M=-M\n")
        elif command == "not":
            self.asm_file.write("M=!M\n")
        else:  # This is a binary command
            self.asm_file.write("D=M\n")  # Save top of stack in D-reg
            self.asm_file.write("A=A-1\n")  # Access second line of stack

            # Binary commands
            if command == "add":
                self.asm_file.write("M=M+D\n")
            elif command == "sub":
                self.asm_file.write("M=M-D\n")
            elif command == "eq":
                self.asm_file.write(EQ_CODE.format(counter=self.counter))
                self.counter += 1
            elif command == "and":
                self.asm_file.write("M=M&D\n")
            elif command == "or":
                self.asm_file.write("M=M|D\n")
            self.asm_file.write(DECREASE_STACK_PTR)  # (*SP)--

    def write_push_pop(self, command: str, segment: str, index: int):
        """
        Writes the Assembly code that is the translation of the given command.
        Command can be either C_PUSH or C_POP
        """
        out_str = ''

        # Set Register to top of stack and save it to R13 and D
        if command == 'pop':
            out_str += ACCESS_STACK + 'D=M\n' + DECREASE_STACK_PTR

        # Locate Segment
        out_str += '@'
        if segment == 'temp':
            out_str += 'R{}\n'.format(5 + index)
        elif segment == 'static':
            out_str += self.vm_file.replace('vm', '') + '{}\n'.format(index)
        elif segment == 'pointer':
            out_str += 'R{}\n'.format(3 + index)
        elif segment == 'constant':
            out_str += '{}\nD=A\n'.format(index)
        else:
            if command == 'pop':
                out_str += 'R13\nM=D\n@'
            out_str += '{}\nD=A\n@'.format(index)
            if segment == 'local':
                out_str += 'R1'
            elif segment == 'argument':
                out_str += 'R2'
            elif segment == 'this':
                out_str += 'R3'
            elif segment == 'that':
                out_str += 'R4'
            out_str += '\nA=D+M\n'  # Sets R14 to segment + index
            if command == 'pop':
                out_str += 'D=A\n'
            else:
                out_str += 'D=M\n'

        if segment in {'temp', 'static', 'pointer'}:
            if command == 'pop':
                out_str += 'M=D\n'
            else:
                out_str += 'D=M\n'

        elif command == 'pop':  # Save the popped value to the desired segment
            out_str += '@R14\nM=D\n@R13\nD=M\n@R14\nA=M\nM=D\n'
            if segment == 'constant':
                out_str = ''

        if command == 'push':  # Assumes the pointer to the value to push is in R14
            out_str += '@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        self.asm_file.write(out_str)

    def write_init(self):
        """Writes the assembly code that effects the VM init"""
        # self.asm_file.write('@256\nD=A\n@SP\nM=D\n')
        # self.write_call('Sys.init', 0)

    def write_label(self, label: str):
        """Writes the assembly code that effects the label code"""
        self.asm_file.write('(' + label + ')\n')

    def write_goto(self, label: str):
        """Writes the assembly code that effects the goto command"""
        self.asm_file.write('@' + label + '\n0;JMP\n')

    def write_if(self, label: str):
        """Writes the assembly code that effects the if-goto command"""
        self.asm_file.write(
            ACCESS_STACK +
            'D=M\n' +  # Save the top value of the stack into D-Reg
            DECREASE_STACK_PTR +
            '@' + label +  # Set the jump location to Label
            '\nD;JNE\n'  # Jump only if the value in D-Reg is not zero
                            )

    def write_call(self, func_name: str, num_args: int):
        """Writes the assembly code that effects the call command"""
        pass

    def write_return(self):
        """Writes the assembly code that effects the return command"""
        pass

    def write_function(self, func_name: str, num_locals: int):
        """Writes the assembly code that effects the function command"""
        pass
