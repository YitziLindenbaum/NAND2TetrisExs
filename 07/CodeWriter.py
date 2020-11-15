ACCESS_STACK = "@SP\nA=M-1\n"  # Sets A-reg at top of stack

EQ_CODE = "D=M-D\n@TRUE\nD;{}\nM=0\n@END_TRUE\n0;JMP\n(TRUE)\nM=-1\
        \n(END_TRUE)\n"

LT_CODE = "@M_NEG\nM;JLT\n@FALSE\nD;JLE\n@SAME_SGN\n0;JMP\n(" \
          "M_NEG)\n@TRUE\nD;JGE\n(SAME_SGN)\nD=M-D\n@TRUE\nD;JLT\n(" \
          "FALSE)\nM=0\n@END\n0;JMP\n(TRUE)\nM=-1\n(END)\n"

GT_CODE = "@M_POS\nM;JGE\n@FALSE\nD;JGE\n@SAME_SGN\n0;JMP\n(" \
          "M_POS)\n@TRUE\nD;JLT\n(SAME_SGN)\nD=M-D\n@TRUE\nD;JGT\n(" \
          "FALSE)\nM=0\n@END\n0;JMP\n(TRUE)\nM=-1\n(END)\n"


def generate_cmp_code(jump):
    """
    Function to easily generate ASM code to perform mathematical comparisons on
    top two levels of stack.
    :param jump: Jump-code (JGT or JLT) to be inserted into the ASM code
    :return: ASM code that performs gt or lt, respectively
    """
    return ("D=M-D\n@TRUE\nD;{}\nM=0\n@END\n0;JMP\n(TRUE)\nM=-1\
        \n(END)\n".format(jump))


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
                code = generate_cmp_code(EQ_CODE)
                self.asm_file.write(code)
            elif command == "gt":
                code = generate_cmp_code(GT_CODE)
                self.asm_file.write(code)
            elif command == "lt":
                code = generate_cmp_code(LT_CODE)
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
