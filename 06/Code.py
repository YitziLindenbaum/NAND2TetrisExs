A_COMMAND = 'a_command'
C_COMMAND = 'c_command'
L_COMMAND = 'l_command'


class Code:

    def __init__(self, parser):
        self.parser = parser

    def processCode(self) -> str:
        """
        :return: Returns the final binary instruction to be written to
        the .Hack file
        """
        if self.parser.commandType() == A_COMMAND:
            return '0' + self.binary()
        elif self.parser.commandType() == C_COMMAND:
            ret = '1' + self.comp() + self.dest() + self.jump()
            return ret
        elif self.parser.commandType() == L_COMMAND:
            pass

    def binary(self):
        """
        Converts symbol given my parser function to 15-bit binary.
        Should only be used for A/L instructions.
        :return: returns 15-digit binary string
        """
        return "{0:015b}".format(int(self.parser.symbol()))

    def __test(self, string, test):
        """
        Private function to easily handle adding bits to binary string.
        :param string: Current binary string
        :param test: bool, should evaluate to True if 1 should be added.
        :return: Binary string with 1 or 0 concatenated on the right.
        """
        if test:
            string += "1"
        else:
            string += "0"
        return string

    def dest(self):
        """
        Handles three dest-bits (instruction[3..5]) of C-instruction.
        :return: string of bits corresponding to given destinations
        """
        dest_asm = self.parser.dest()
        dest_bin = ""

        dest_bin = self.__test(dest_bin, "A" in dest_asm)  # bit 5
        dest_bin = self.__test(dest_bin, "D" in dest_asm)  # bit 4
        dest_bin = self.__test(dest_bin, "M" in dest_asm)  # bit 3

        return dest_bin

    def comp(self):
        """
        Handles nine comp-bits (instruction[6..14]) of C-instruction.
        :return: string of bits corresponding to given computation
        """
        comp_asm = self.parser.comp()
        comp_bin = ""

        # instruction[14..13]
        if "<<" in comp_asm or ">>" in comp_asm:
            comp_bin += "01"
        else:
            comp_bin += "11"

        # instruction[12]
        if "M" in comp_asm:
            comp_bin += "1"
            # Replace 'M' with 'A' for simplicity in later bits
            comp_asm = comp_asm.replace("M", "A")
        else:
            comp_bin += "0"

        # instruction[11] (ZX or shift_left)
        comp_bin = self.__test(comp_bin, "<<" in comp_asm or ("D" not in
                                    comp_asm and ">>" not in comp_asm))
        # instruction[10] (NX or shift D)
        instruction10_yes = {"1", "-1", "A", "!A", "-A", "D+1", "A+1",
                             "A-1", "D-A", "D|A", "D>>", "D<<"}
        comp_bin = self.__test(comp_bin, comp_asm in instruction10_yes)

        # append zeroes and stop if shift command
        if "<<" in comp_asm or ">>" in comp_asm:
            return comp_bin + "0000"

        # instruction[9] (ZY)
        comp_bin = self.__test(comp_bin, "A" not in comp_asm)

        # instruction[8] (NY)
        instruction8_yes = {"1", "D", "!D", "-D", "D+1", "A+1", "D-1",
                            "A-D", "D|A"}
        comp_bin = self.__test(comp_bin, comp_asm in instruction8_yes)

        # instruction[7] (F)
        instruction7_any = {"1", "0", "-", "+"}
        comp_bin = self.__test(comp_bin, any(char in comp_asm
                                             for char in instruction7_any))

        # instruction[6] (NO)
        instruction6_yes = {"1", "!D", "!A", "-D", "-A", "D+1", "A+1", "D-A",
                            "A-D", "D|A"}
        comp_bin = self.__test(comp_bin, comp_asm in instruction6_yes)

        return comp_bin

    def jump(self):
        """
        Handles three jump-bits (instruction[0..2]) of C-instruction.
        :return: String of bits corresponding to given jump command
        """
        jump_asm = self.parser.jump()
        jump_bin = ""

        jump_bin = self.__test(jump_bin,
                               jump_asm in {"JLT", "JNE", "JLE", "JMP"})
        jump_bin = self.__test(jump_bin,
                               jump_asm in {"JEQ", "JGE", "JLE", "JMP"})
        jump_bin = self.__test(jump_bin,
                               jump_asm in {"JGT", "JGE", "JNE", "JMP"})

        return jump_bin
