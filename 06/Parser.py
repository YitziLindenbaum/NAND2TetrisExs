COMMENT_HEADER = '//'
A_COMMAND_HEADER = '@'
L_COMMAND_HEADER = '('
L_COMMAND_FOOTER = ')'
A_COMMAND = 'a_command'
C_COMMAND = 'c_command'
L_COMMAND = 'l_command'
SUCCESSFUL_SPLIT = 2


class Parser:
    """
    Usage notes:
        (1) The parser starts before the beginning of the file. In other words, advance() needs to be called before the
            parser will begin to parse anything
        (2) No validity checks are performed. So make sure to call hasNextCommand() before calling advance()
        (3) If WLOG comp() is called when commandType() == A_COMMAND, then an empty string is returned
        (4) The constructor receives an already opened file.
            The user is responsible to close it.
            Can be closed immediately after the constructor is called.
    """

    def __init__(self, file_obj):
        """
        :param file_obj: A file object -- already opened
        """
        self.table = dict()
        for i in range(16):  # Init R0 - R15
            key = 'R' + str(i)
            self.table[key] = i
        constants = [('SP', 0), ('LCL', 1), ('ARG', 2), ('THIS', 3), ('THAT', 4), ('SCREEN', 16384), ('KBD', 24576)]
        for key, value in constants:
            self.table[key] = value

        self.file_obj = file_obj
        self.lines = []
        self.preprocess()
        self.current_command = -1  # Init so there is no current command
        self.command_type: str = ''
        self._jump: str = ''
        self._symbol: str = ''
        self._dest: str = ''
        self._comp: str = ''
        self.table_counter = 16

    def get_table(self):
        return self.table

    def preprocess(self):
        """
        Iterates through the file, removes all comments and whitespaces,
        and stores the resulting list of strings in self.lines
        """
        all_lines = self.file_obj.readlines()  # Read all lines of the file into a list
        line_number = 0
        for line in all_lines:
            line = ''.join(line.split())  # Remove all whitespaces from the line

            if COMMENT_HEADER in line:  # If a comment exists in the line

                # This will return a list of form ['', 'comment_content'] or ['code_content', 'comment_content']
                # In both cases, we are interested only in the item at the zero index
                parts = line.split(COMMENT_HEADER)
                line = parts[0]

            if L_COMMAND_HEADER in line:
                symbol = line[1:-1]  # remove parens
                if symbol not in self.table:
                    self.table[symbol] = line_number
                line = ''

            if line != '':
                self.lines.append(line)
                line_number += 1

    def parseLine(self):
        """
        Parses the current command and stores the relevant parts in their respective fields
        """
        self._symbol, self._comp, self._jump, self._dest = '', '', '', ''

        line = self.lines[self.current_command]
        constants = []

        if A_COMMAND_HEADER in line:  # We have a line of form: '@value'
            self.command_type = A_COMMAND
            _split = line.split(A_COMMAND_HEADER)  # Will return a list of form: ['', 'value']
            self._symbol = _split[1]

            if self._symbol in self.table:
                self._symbol = self.table[self._symbol]
            elif not self._symbol.isnumeric():
                self.table[self._symbol] = self.table_counter
                self._symbol = self.table_counter
                self.table_counter += 1

        elif L_COMMAND_HEADER in line and L_COMMAND_FOOTER in line:  # We have a line of form (Xxx)
            self.command_type = L_COMMAND
            self._symbol = line[1:len(line) - 1]  # Strip the parenthesis from the symbol
        else:  # We have a C-instruction
            self.command_type = C_COMMAND

            equal_split = line.split('=')
            if len(equal_split) == SUCCESSFUL_SPLIT:  # If '=' was in the line
                self._dest = equal_split[0]
                line = equal_split[1]

            semicolon_split = line.split(';')
            if len(semicolon_split) == SUCCESSFUL_SPLIT:  # If there was a semicolon in the line
                self._jump = semicolon_split[1]
            self._comp = semicolon_split[0]

    def hasMoreCommands(self) -> bool:
        """Boolean to test if there are any more commands to parse"""
        return self.current_command < len(self.lines) - 1

    def advance(self):
        """
        Reads the next command from the input and sets it as the current command.
        Then will parse the command and store the relevant parts in their respective fields
        Should only be called if hasMoreCommands() is True; otherwise, behavior is undefined
        """
        self.current_command += 1
        self.parseLine()

    def commandType(self):
        """
        Returns the type of command that defines the current command
        :return: A_COMMAND, C_COMMAND, or L_COMMAND constants
        """
        return self.command_type

    def symbol(self) -> str:
        """
        Returns the symbol or decimal Xxx of the current command (which will be @Xxx or (Xxx))
        Should be called only when commandType() is A_COMMAND or L_COMMAND
        :return: The Xxx or @Xxx or (Xxx) as a string
        """
        return self._symbol

    def dest(self) -> str:
        """
        Returns the 'dest' part of the C-instruction. There are 8 possibilities
        Should only be called when commandType() is C_COMMAND
        :return: The 'dest' mnemonic as a string
        """
        return self._dest

    def comp(self) -> str:
        """
        Returns the 'comp' part of the C-instruction. There are 28 possibilities
        Should only be called when commandType() is C_COMMAND
        :return: The 'comp' mnemonic as a string
        """
        return self._comp

    def jump(self) -> str:
        """
        Returns the 'jump' part of the C-instruction. There are 8 possibilities
        Should only be called when commandType() is C_COMMAND
        :return: The 'jump' mnemonic as a string
        """
        return self._jump

