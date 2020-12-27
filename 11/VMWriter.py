SEGMENTS = {'const', 'arg', 'local', 'static', 'this', 'that', 'pointer', 'temp'}
COMMANDS = {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'}


class VMWriter:

    def __init__(self, outfile):
        self.outfile = outfile

    def write_push(self, segment: str, index: int):
        """
        Writes a VM push command.
        Args:
            segment: Can be any of the strings listed in SEGMENTS
            index: An int to accompany the segment
        """
        pass

    def write_pop(self, segment: str, index: int):
        """
        Writes a VM pop command.
        Args:
            segment: Can be any of the strings listed in SEGMENTS
            index: An int to accompany the segment
        """
        pass

    def write_arithmetic(self, command: str):
        """
        Writes a VM arithmetic command.
        Args:
            command: Can be any of the strings listed in COMMANDS
        """
        pass

    def write_label(self, label: str):
        """
        Writes a VM label command.
        Args:
            label: A string for the label
        """
        pass

    def write_goto(self, label: str):
        """
        Writes a VM goto command.
        Args:
            label: A string for the label
        """
        pass

    def write_if(self, label: str):
        """
        Writes a VM if-goto command.
        Args:
            label: A string for the label
        """
        pass

    def write_call(self, name: str, n_args: int):
        """
        Writes a VM call command.
        Args:
            name: A string for the name of the subroutine
            n_args: The number of arguments the subroutine accepts
        """
        pass

    def write_function(self, name: str, n_locals: int):
        """
        Writes a VM function command.
        Args:
            name: A string for the name of the subroutine
            n_locals: The number of local variables the function has
        """
        pass

    def write_return(self):
        """
        Writes a VM return command.
        """
        pass
