COMMENT_HEADER = '//'
C_ARITHMETIC = 'arithmetic'
C_PUSH = 'push'
C_POP = 'pop'
C_LABEL = 'label'
C_GOTO = 'goto'
C_IF = 'if-goto'
C_FUNCTION = 'function'
C_RETURN = 'return'
C_CALL = 'call'
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
SEGMENTS = {
    'argument',
    'local',
    'static',
    'constant',
    'this',
    'that',
    'pointer',
    'temp'
}
MEMORY_ACCESS_COMMANDS = {C_PUSH, C_POP}
PROGRAM_FLOW_COMMANDS = {C_LABEL, C_GOTO, C_IF}
FUNCTION_CALLING_COMMANDS = {C_FUNCTION, C_CALL, C_RETURN}
TRUE = 0
FALSE = -1


class Parser:

    def __init__(self, file_obj):
        """
        :param file_obj: An already opened VM file object. This module is not responsible for closing it
        """
        self.file_obj = file_obj
        self.lines = []
        self.preprocess()
        self.current_command = -1  # Init so there is no current command
        self._command_type: str = ''
        self._arg1: str = ''
        self._arg2: str = ''

    def preprocess(self):
        """
        Iterates through the file, removes all comments and whitespaces,
        and stores the resulting list of strings in self.lines
        """
        all_lines = self.file_obj.readlines()  # Read all lines of the file into a list
        line_number = 0
        for line in all_lines:
            line = ' '.join(line.split())

            if COMMENT_HEADER in line:  # If a comment exists in the line

                # This will return a list of form ['', 'comment_content'] or ['code_content', 'comment_content']
                # In both cases, we are interested only in the item at the zero index
                parts = line.split(COMMENT_HEADER)
                line = parts[0].strip()

            if line != '':
                self.lines.append(line)
                line_number += 1

    def has_more_commands(self) -> bool:
        """Returns True iff there are more commands left in the file"""
        return self.current_command < len(self.lines) - 1

    def advance(self):
        """
        Reads the next command from the input and sets it as the current command.
        Then will parse the command and store the relevant parts in their respective fields
        Should only be called if hasMoreCommands() is True; otherwise, behavior is undefined
        """
        self.current_command += 1
        self.parse_line()

    def parse_line(self):
        """
        Parses the current command and stores the relevant parts in their respective fields
        """
        self._command_type, self._arg1, self._arg2 = '', '', ''
        parts = self.lines[self.current_command].split()
        if len(parts) == 1:
            if parts[0] in ARITHMETIC_COMMANDS:
                self._command_type = C_ARITHMETIC
                self._arg1 = parts[0]
            else:  # parts[0] == 'return'
                self._command_type = C_RETURN

        else:  # len(parts) is 2 or 3
            self._command_type = parts[0]
            self._arg1 = parts[1]

            if len(parts) == 3:
                self._arg2 = parts[2]

    def command_type(self) -> str:
        """Returns the type of the current VM command"""
        return self._command_type

    def arg1(self) -> str:
        """
        Returns the first argument of the current command.
        In the case of C_ARITHMETIC, the command itself is returned.
        Should not be called if the current command is C_RETURN
        """
        return self._arg1

    def arg2(self) -> str:
        """
        Returns the second argument of the current command.
        Should be called only if the current command is:
            - C_PUSH
            - C_POP
            - C_FUNCTION
            - C_CALL
        """
        return self._arg2
