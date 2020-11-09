A_COMMAND = 'a_command'
C_COMMAND = 'c_command'
L_COMMAND = 'l_command'


class Code:

    def __init__(self, parser):
        self.parser = parser

    def processCode(self) -> str:
        """
        :return: Returns the final binary instruction to be written to the .Hack file
        """
        if self.parser.commandType() == A_COMMAND:
            return '0' + self.binary()
        elif self.parser.commandType() == C_COMMAND:
            ret = '1' + self.comp() + self.dest() + self.jump()
            return ret
        elif self.parser.commandType() == L_COMMAND:
            pass

    def binary(self):
        return "{0:015b}".format(int(self.parser.symbol()))  # check that there won't
        # be overload with int

    def test(self, string, test):
        if test:
            string += "1"
        else:
            string += "0"
        return string

    def dest(self):
        dest_asm = self.parser.dest()
        dest_bin = ""

        dest_bin = self.test(dest_bin, "A" in dest_asm)
        dest_bin = self.test(dest_bin, "D" in dest_asm)
        dest_bin = self.test(dest_bin, "M" in dest_asm)

        return dest_bin

    def comp(self):
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
            comp_asm.replace("M", "A")
        else:
            comp_bin += "0"

        # instruction[11] (ZX or shift_left)
        comp_bin = self.test(comp_bin, "D" not in comp_asm or "<<" in comp_asm)

        # instruction[10] (NX or shift D)
        instruction10_yes = {"1", "-1", "A", "!A", "-A", "D+1", "A+1",
                             "A-1", "D-A", "D|A", "D>>", "D<<"}
        comp_bin = self.test(comp_bin, comp_asm in instruction10_yes)

        # append zeroes and stop if shift command
        if "<<" in comp_asm or ">>" in comp_asm:
            return comp_bin + "0000"

        # instruction[9] (ZY)
        comp_bin = self.test(comp_bin, "A" not in comp_asm)

        # instruction[8] (NY)
        instruction8_yes = {"1", "D", "!D", "-D", "D+1", "A+1", "D-1",
                            "A-D", "D|A"}
        comp_bin = self.test(comp_bin, comp_asm in instruction8_yes)

        # instruction[7] (F)
        instruction7_any = {"1", "0", "-", "+"}
        comp_bin = self.test(comp_bin, any(char in comp_asm for char in instruction7_any))

        # instruction[6] (NO)
        instruction6_yes = {"1", "!D", "!A", "-D", "-A", "D+1", "A+1", "D-A",
                            "A-D", "D|A"}
        comp_bin = self.test(comp_bin, comp_asm in instruction6_yes)

        return comp_bin

    def jump(self):
        jump_asm = self.parser.jump()
        jump_bin = ""
        print("jump_asm: ", jump_asm)
        jump_bin = self.test(jump_bin, jump_asm in {"JLT", "JNE", "JLE", "JMP"})
        jump_bin = self.test(jump_bin, jump_asm in {"JEQ", "JGE", "JLE", "JMP"})
        jump_bin = self.test(jump_bin, jump_asm in {"JGT", "JGE", "JNE", "JMP"})
        print("jump_bin: ", jump_bin)

        return jump_bin
