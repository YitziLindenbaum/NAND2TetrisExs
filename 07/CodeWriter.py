class CodeWriter:

    def __init__(self, file):
        """
        :param file: An already opened Assembly file to write to
        """
        self.asm_file = file

    def set_file_name(self, file_name: str):
        """
        Informs the code writer that the translation of the new VM file has started
        """
        pass

    def write_arithmetic(self, command: str):
        """Writes the assembly code that is the translation of the given command"""
        pass

    def write_push_pop(self, command: str, segment: str, index: int):
        """
        Writes the Assembly code that is teh translation of the given command.
        Command can be either C_PUSH or C_POP
        """
        pass

    def close(self):
        """Closes the output file"""
        pass
