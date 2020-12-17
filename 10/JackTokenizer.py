import re
from typing import List

KEYWORDS = {'class', 'constructor', 'function', 'method', 'field', 'static', 'var',
            'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let',
            'do', 'if', 'else', 'while', 'return'}
SYMBOLS = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'}


class Token:

    def __init__(self, token_type: str, content: str):
        self.token_type: str = token_type
        self.content: str = content

    def get_token_type(self) -> str:
        return self.token_type

    def get_content(self) -> str:
        return self.content


class JackTokenizer:
    """
    Removes all comments and white space from the input stream,
    and breaks it into Jack-language tokens, as specified by the Jack grammar.
    """

    def __init__(self, input_file):
        self.file = input_file
        self.file_str: str = self.read_file_to_str()
        self.tokens: List[Token] = []
        self.current_command = -1
        self._token_type: str = ''
        self._key_word: str = ''
        self._symbol: str = ''
        self._identifier: str = ''
        self._int_val: str = ''
        self._string_val: str = ''
        self.parse_file_str()

    def read_file_to_str(self) -> str:
        """Translates self.file into one long string while removing comments and empty lines"""
        out_str: str = ''
        lines = self.file.readlines()
        for line in lines:
            full_line_comment = re.search('\A[\s]*[/*]', line)
            mid_line_comment = re.search('(.+)([\s]*//.*)', line)
            blank_line = re.search('\A[\s]+\Z', line)
            if full_line_comment or blank_line:
                continue
            elif mid_line_comment:
                out_str += mid_line_comment[1]
            else:
                out_str += line
        return out_str

    def parse_file_str(self):
        """Parse self.file_str into tokens and stores them in self.tokens"""
        split_with_whitespace = re.split('(\W)', self.file_str)
        in_string_constant = False
        str_const = ''
        for item in split_with_whitespace:
            if in_string_constant:

                if item == '"':  # If we have reached the end of the string
                    self.tokens.append(Token('string_const', str_const))
                    str_const = ''
                    in_string_constant = False
                else:
                    str_const += item

            elif item.strip():  # If the item is not whitespace
                if item in KEYWORDS:
                    self.tokens.append(Token('keyword', item))
                elif item in SYMBOLS:
                    self.tokens.append(Token('symbol', item))
                elif item.isdigit():
                    self.tokens.append(Token('int_const', item))
                elif item == '"':
                    in_string_constant = True
                else:
                    self.tokens.append(Token('identifier', item))

    def has_more_tokens(self) -> bool:
        """Returns True iff there are more tokens in the input file"""
        return self.current_command < len(self.tokens) - 1

    def advance(self):
        """
        Gets the next token from the input and makes it the current token.
        This method should only be called if has_more_tokens() returns True.
        Initially there is no current token.
        """
        self.current_command += 1

    def token_type(self) -> str:
        """
        Returns the type of the current token
        Possible types are:
            (1) KEYWORD
            (2) SYMBOL
            (3) IDENTIFIER
            (4) INT_CONST
            (5) STRING_CONST
        """
        return self.tokens[self.current_command].get_token_type()

    def key_word(self) -> str:
        """
        Returns the keyword which is the current token.
        Should only be called when token_type() is KEYWORD.
        Possible keys are:
            (1) CLASS
            (2) METHOD
            (3) FUNCTION
            (4) CONSTRUCTOR
            (5) INT
            (6) BOOLEAN
            (7) CHAR
            (8) VOID
            (9) VAR
            (10) STATIC
            (11) FIELD
            (12) LET
            (13) DO
            (14) IF
            (15) ELSE
            (16) WHILE
            (17) RETURN
            (18) TRUE
            (19) FALSE
            (20) NULL
            (21) THIS
        """
        return self.tokens[self.current_command].get_content()

    def symbol(self) -> str:
        """
        Returns the character which is the current token.
        Should be called only when token_type() is SYMBOL
        """
        return self.tokens[self.current_command].get_content()

    def identifier(self) -> str:
        """
        Returns the identifier which is the current token.
        Should be called only when token_type() is IDENTIFIER
        """
        return self.tokens[self.current_command].get_content()

    def int_val(self) -> str:
        """
        Returns the integer value (as a string representation) which is the current token.
        Should be called only when token_type() is INT_CONST
        """
        return self.tokens[self.current_command].get_content()

    def string_val(self) -> str:
        """
        Returns the string value which is the current token.
        Should be called only when token_type() is STRING_CONST
        """
        return self.tokens[self.current_command].get_content()
