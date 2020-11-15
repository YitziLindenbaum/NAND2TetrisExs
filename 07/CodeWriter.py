ACCESS_STACK = "@SP\nA=M-1\n"  # Sets A-reg at top of stack


def generate_cmp_code(jump):
    """
    Function to easily generate ASM code to perform mathematical comparisons on
    top two levels of stack.
    :param jump: Jump-code (JEQ, JGT, or JLT) to be inserted into the ASM code
    :return: ASM code that performs eq, gt, or lt respectively
    """
    return("D=M-D\n@TRUE\nD;{}\nM=0\n@END_TRUE\n0;JMP\n(TRUE)\nM=-1\
        \n(END_TRUE)\n".format(jump))


ARITHMETIC_COMMANDS = {
    'add',
    'sub',
    'neg',
    'eq',
    'gt',
    'lt',
    'and',
    'or',
    'not'
}


class CodeWriter:

    def __init__(self, file):
        """
        :param file: An already opened Assembly file to write to
        """
        self.asm_file = file
        self.vm_file = None

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
        # Unitary commands
        if command == "neg":
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
                code = generate_cmp_code("JEQ")
                self.asm_file.write(code)
            elif command == "gt":
                code = generate_cmp_code("JGT")
                self.asm_file.write(code)
            elif command == "lt":
                code = generate_cmp_code("JLT")
                self.asm_file.write(code)
            elif command == "and":
                self.asm_file.write("M=M&D\n")
            elif command == "or":
                self.asm_file.write("M=M|D\n")

            self.asm_file.write("@SP\nM=M-1\n")  # (*SP)--

    def write_push_pop(self, command: str, segment: str, index: int):
        """
        Writes the Assembly code that is teh translation of the given command.
        Command can be either C_PUSH or C_POP
        """
        pass

    def close(self):
        """Closes the output file"""
        pass
