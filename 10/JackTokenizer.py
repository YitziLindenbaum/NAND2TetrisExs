class JackTokenizer:
    """
    Removes all comments and white space from the input stream,
    and breaks it into Jack-language tokens, as specified by the Jack grammar.
    """

    def __init__(self, input_file):
        self.file = input_file
        self.tokens = []  # todo Do some preprocessing that breaks the entire file into tokens (w/o analyzing them)
        self.current_command = -1
        self._token_type: str = ''
        self._key_word: str = ''
        self._symbol: str = ''
        self._identifier: str = ''
        self._int_val: str = ''
        self._string_val: str = ''

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
        # todo Add a call to a function that parses the next token

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
        return self._token_type

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
        return self._key_word

    def symbol(self) -> str:
        """
        Returns the character which is the current token.
        Should be called oinly when token_type() is SYMBOL
        """
        return self._symbol

    def identifier(self) -> str:
        """
        Returns the identifier which is the current token.
        Should be called oinly when token_type() is IDENTIFIER
        """
        return self._identifier

    def int_val(self) -> str:
        """
        Returns the integer value (as a string representation) which is the current token.
        Should be called only when token_type() is INT_CONST
        """
        return self._int_val

    def string_val(self) -> str:
        """
        Returns the string value which is the current token.
        Should be called oinly when token_type() is STRING_CONST
        """
        return self._string_val
