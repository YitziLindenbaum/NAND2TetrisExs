

class Code:

    def __init__(self, mnemonic):
        self.mnemonic = mnemonic

    def test(self, string, test):
        if test:
            string += "1"
        else:
            string += "0"

    def dest(self):
        dest_asm = self.mnemonic.dest()
        dest_bin = ""

        self.test(dest_bin, "A" in dest_asm)
        self.test(dest_bin, "D" in dest_asm)
        self.test(dest_bin, "M" in dest_asm)

        return dest_bin

    def comp(self):
        comp_asm = self.mnemonic.comp()
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
        self.test(comp_bin, "D" not in comp_asm or "<<" in comp_asm)

        # instruction[10] (NX or shift D)
        instruction10_yes = {"1", "-1", "A", "!A", "-A", "D+1", "A+1",
                             "A-1", "D-A", "D|A", "D>>", "D<<"}
        self.test(comp_bin, comp_asm in instruction10_yes)

        # append zeroes and stop if shift command
        if "<<" in comp_asm or ">>" in comp_asm:
            return comp_bin + "0000"

        # instruction[9] (ZY)
        self.test(comp_bin, "A" not in comp_asm)

        # instruction[8] (NY)


    def jump(self):
        jump_asm = self.mnemonic.jump()
        jump_bin = ""

        self.test(jump_bin, jump_asm in {"JLT", "JNE", "JLE", "JMP"})
        self.test(jump_bin, jump_asm in {"JEQ", "JGE", "JLE", "JMP"})
        self.test(jump_bin, jump_asm in {"JGT", "JGE", "JNE", "JMP"})

        return jump_bin


if __name__ == 'main':
    pass
