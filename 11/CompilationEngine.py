st = __import__('SymbolTable')
vw = __import__('VMWriter')
NEWLINE = '\n'
OPS = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
ARG = 'arg'
VAR = 'var'
THIS = 'this'
METHOD = 'method'
STATIC = 'static'
FIELD = 'field'
CONSTRUCTOR = 'constructor'
FUNCTION = 'function'
ELSE = 'else'
CONSTANT = 'constant'
POINTER = 'pointer'


class CompilationEngine:
    """
    Effects the actual compilation output.
    It receives it input from the JackTokenizer and emits
    its parsed structure into an output file
    """

    def __init__(self, tokenizer_object, output_file):
        self.tokenizer = tokenizer_object
        self.output_file = output_file
        self.class_name: str = ''
        self.symbol_table = st.SymbolTable()
        self.vm_writer = vw.VMWriter(self.output_file)
        self.compile_class()

    def compile_class(self):
        """Compiles a complete class"""
        if not self.tokenizer.has_more_tokens():  # empty file (necessary?)
            return

        self._advance_n_times(2)  # Advance over the class keyword
        self.class_name = self._get_next_token()
        self._advance_n_times(1)  # Advance over the opening bracket

        while self.tokenizer.keyword() in {STATIC, FIELD}:
            self.compile_class_var_dec()

        while self.tokenizer.keyword() in {CONSTRUCTOR, FUNCTION, METHOD}:
            self.compile_subroutine()

        self._advance_n_times(1)  # Advance past the }

    def _get_next_token(self):
        _next = self.tokenizer.identifier()
        self.tokenizer.advance()
        return _next

    def _advance_n_times(self, n=1):
        """Advances the tokenizer n times. Default is once"""
        for _ in range(n):
            self.tokenizer.advance()

    def compile_class_var_dec(self):
        """Adds all of the static and field variables to the symbol table"""
        _kind = self._get_next_token()
        _type = self._get_next_token()
        _name = self._get_next_token()

        while self.tokenizer.symbol() == ',':  # multiple varDecs in one line
            self.tokenizer.advance()  # Advance past the comma
            self.symbol_table.define(_name, _type, _kind)
            _name = self._get_next_token()

        self.symbol_table.define(_name, _type, _kind)
        self.tokenizer.advance()  # Advance past the ';'

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor"""
        routine_type = self._get_next_token()  # Can be constructor, function, or method
        return_type = self._get_next_token()  # Can be a keyword (including void) or a user defined type
        func_name = self._get_next_token()

        self._advance_n_times(1)  # Advance past the (
        self.symbol_table.start_subroutine()  # init the symbol table for the subroutine
        if routine_type == METHOD:  # Include the 'this' object as the first parameter
            self.symbol_table.define(THIS, self.class_name, ARG)
        self.compile_parameter_list()
        self._advance_n_times(1)  # Advance past the )

        self.vm_writer.write_function(self.class_name + '.' + func_name, self.symbol_table.var_count(ARG))
        if routine_type == CONSTRUCTOR:
            self.vm_writer.write_push(CONSTANT, self.symbol_table.var_count(FIELD))
            self.vm_writer.write_call('Memory.alloc', 1)

        elif routine_type == METHOD:
            self.vm_writer.write_push(self.symbol_table.kind_of(THIS), self.symbol_table.index_of(THIS))
            self.vm_writer.write_pop(POINTER, 0)

        self._advance_n_times(1)  # Advance past the '{'
        while self.tokenizer.keyword() == VAR:
            self.compile_var_dec()
        self.compile_statements()
        self._advance_n_times(1)  # Advance past the '}'

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing '()'"""
        while self.tokenizer.symbol() != ')':
            _kind = ARG
            _type = self._get_next_token()
            _name = self._get_next_token()

            if self.tokenizer.symbol() == ',':
                self._advance_n_times(1)  # Advance past the comma
                self.symbol_table.define(_name, _type, _kind)
                _type = self._get_next_token()
                _name = self._get_next_token()

            self.symbol_table.define(_name, _type, _kind)

    def compile_var_dec(self):
        """Compiles a var declaration"""
        _kind = self._get_next_token()  # Will always be 'var'
        _type = self._get_next_token()  # Can be either a built in or user defined
        _name = self._get_next_token()

        while self.tokenizer.symbol() == ',':  # multiple varDecs in one line
            self.symbol_table.define(_name, _type, _kind)
            self._advance_n_times(1)  # Advance past the comma
            _name = self._get_next_token()

        self.symbol_table.define(_name, _type, _kind)
        self._advance_n_times(1)  # Advance past the ';'

    def compile_statements(self):
        """Compiles a sequence of statements, not including the enclosing '()'"""
        statement_dict = {
            "do": self.compile_do,
            "let": self.compile_let,
            "while": self.compile_while,
            "return": self.compile_return,
            "if": self.compile_if
        }
        while self.tokenizer.keyword() in statement_dict:
            statement_dict[self.tokenizer.keyword()]()

    def compile_do(self):
        """Compiles a do statements"""
        self._advance_n_times(1)  # Advance over the 'do' keyword
        func_name = self._get_next_token()

        if self.tokenizer.symbol() == '.':  # We are calling a method of another class or a static method of our class
            self._advance_n_times(1)  # Advance past the '.'
            func_name = func_name + '.' + self._get_next_token()
            instance_call = False
        else:  # We are calling a subroutine of the current instance
            instance_call = True
            func_name = self.class_name + '.' + func_name
            self.vm_writer.write_push(self.symbol_table.kind_of(THIS), self.symbol_table.index_of(THIS))  # Push 'this' to the stack

        self._advance_n_times(1)  # Advance past the '('
        num_params = self.compile_expression_list()
        self._advance_n_times(2)  # Advance past the ');'

        self.vm_writer.write_call(func_name, num_params + instance_call)

    def compile_let(self):
        """Compiles a let statement"""
        self._advance_n_times(1)
        var_name = self._get_next_token()

        if self.tokenizer.symbol() == '[':  # array index TODO
            self._add_symbol()  # '['
            self.compile_expression()
            self._add_symbol()  # ']'

        self._advance_n_times(1)  # Advance past the '='
        self.compile_expression()  # Will be responsible for pushing the value to the top of the stack

        # Pop the top value of the stack into the desired variable
        stack_kind = self.get_pointer_type_from_kind(var_name)
        pointer_index = self.symbol_table.index_of(var_name)
        self.vm_writer.write_pop(stack_kind, pointer_index)

        self._advance_n_times(1)  # Advance past the ';'

    def compile_while(self):
        """Compiles a while statement"""
        self._add_keyword()  # "while"
        self._advance_n_times(1)  # Advance past the '('
        self.compile_expression()
        self._advance_n_times(2)  # Advance past the ) and '{'
        self.compile_statements()
        self._advance_n_times(1)  # Advance past the '}'

    def compile_return(self):
        """Compiles a return statement"""
        self._add_keyword()  # "return"
        if not self.tokenizer.symbol() == ';':
            self.compile_expression()
        self._advance_n_times(1)  # Advance past the ';'

    def compile_if(self):
        """Compiles an if statement, possibly with a trailing else clause"""
        self._add_keyword()  # "if"
        self._advance_n_times(1)  # Advance past the '('
        self.compile_expression()
        self._advance_n_times(2)  # Advance past the ')' and {
        self.compile_statements()
        self._advance_n_times(1)  # Advance past the '}'

        if self.tokenizer.keyword() == ELSE:
            self._add_keyword()  # "else"
            self._advance_n_times(1)  # Advance past the '{'
            self.compile_statements()
            self._advance_n_times(1)  # Advance past the '}'

    def compile_expression(self):
        """Compiles an expression"""
        self.compile_term()
        if self.tokenizer.symbol() in OPS:
            self._add_symbol()  # binary operator
            self.compile_term()

    def compile_term(self):
        """
        Compiles a term.
        If the current token is an identifier, the routine must distinguish between
        a variable, an array entry, and a subroutine call.
        A single look ahead token, which may be '[', '(', or '.' suffices
        to distinguish between the three possibilities.
        Any other token is not part of this term and should not be advanced over.
        """
        _token_type = self.tokenizer.token_type()
        if _token_type == 'string_const':
            self._add_xml_node('stringConstant', self.tokenizer.string_val())
            self.tokenizer.advance()
        elif _token_type == 'int_const':
            self.vm_writer.write_push(CONSTANT, self._get_next_token())
        elif _token_type == 'keyword':
            self._add_keyword()
        elif _token_type == 'identifier':
            _name = self._get_next_token()
            if self.tokenizer.symbol() == '.':  # subroutine call
                self._advance_n_times(1)  # Advance past the '.'
                func_name = self._get_next_token()
                stack_kind = self.get_pointer_type_from_kind(_name)
                if stack_kind:  # This is a method or a constructor
                    self.vm_writer.write_push()  # todo push the 'this' pointer properly
                self._advance_n_times(1)  # Advance past the '('
                num_args = self.compile_expression_list()  # params
                self._advance_n_times(1)  # Advance past the ')'
                call_name = _name + '.' + func_name

                if not stack_kind or func_name == 'new':  # function or constructor call (i.e not method)
                    self.vm_writer.write_call(call_name, num_args + (func_name == 'new'))
                else:  # a method call of another class
                    self.vm_writer.write_push(stack_kind, self.symbol_table.index_of(_name))
                    self.vm_writer.write_call(call_name, num_args + 1)

            elif self.tokenizer.symbol() == '[':  # array entry
                self._add_symbol()  # '['
                self.compile_expression()
                self._add_symbol()  # ']'
            elif self.tokenizer.symbol() == '(':  # a method of this class
                self._advance_n_times(1)
                num_args = self.compile_expression_list()  # params
                self._advance_n_times(1)  # Advance past the ')'
                call_name = self.class_name + '.' + _name

                self.vm_writer.write_call(call_name, num_args)

        elif _token_type == 'symbol':
            if self.tokenizer.symbol() == '(':
                self._advance_n_times(1)  # Advance past the '('
                self.compile_expression()
                self._advance_n_times(1)  # Advance past the ')'
            else:
                self._add_symbol()  # unary op
                self.compile_term()

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions"""
        num_expressions = 0
        if self.tokenizer.symbol() != ')':  # non-empty list
            self.compile_expression()
            num_expressions += 1
            while self.tokenizer.symbol() == ',':
                self._add_symbol()  # ','
                self.compile_expression()
                num_expressions += 1
        return num_expressions
