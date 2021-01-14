st = __import__('SymbolTable')
vw = __import__('VMWriter')

NEWLINE = '\n'
OPS = {
    '+': 'add',
    '-': 'sub',
    '*': 'call Math.multiply 2',
    '/': 'call Math.divide 2',
    '&': 'and',
    '|': 'or',
    '<': 'lt',
    '>': 'gt',
    '=': 'eq',
    '~': 'not'
}
ARG = 'arg'
NOT = 'not'
VAR = 'var'
ADD = 'add'
THIS = 'this'
THAT = 'that'
TEMP = 'temp'
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
        self.if_counter: int = 0
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

        self._advance_n_times(1)  # Advance past the '{'
        while self.tokenizer.keyword() == VAR:
            self.compile_var_dec()

        num_vars = self.symbol_table.var_count(ARG) + self.symbol_table.var_count(VAR)
        self.vm_writer.write_function(self.class_name + '.' + func_name, num_vars)
        if routine_type == CONSTRUCTOR:
            self.vm_writer.write_push(CONSTANT, self.symbol_table.var_count(FIELD))
            self.vm_writer.write_call('Memory.alloc', 1)
            self.vm_writer.write_pop(POINTER, 0)  # anchor 'this' at memory
            # block returned by alloc
            # todo: constructor will end with Jack code "return this" --
            #  make sure this is handled properly by compile_term (should
            #  compile to "push pointer 0 / return")

        elif routine_type == METHOD:
            self.vm_writer.write_push(self.symbol_table.get_pointer_type_from_kind(THIS), self.symbol_table.index_of(THIS))
            self.vm_writer.write_pop(POINTER, 0)

        self.compile_statements()
        self._advance_n_times(1)  # Advance past the '}'

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing '()'"""
        while self.tokenizer.symbol() != ')':
            _kind = ARG
            _type = self._get_next_token()
            _name = self._get_next_token()

            while self.tokenizer.symbol() == ',':
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
            instance_call = False
            self._advance_n_times(1)  # Advance past the '.'
            _kind = self.symbol_table.get_pointer_type_from_kind(func_name)
            new_func_name = self._get_next_token()
            if _kind:
                self.vm_writer.write_push(_kind, self.symbol_table.index_of(func_name))
                func_name = self.symbol_table.type_of(func_name)
                instance_call = True
            call_name = func_name + '.' + new_func_name
        else:  # We are calling a subroutine of the current instance
            instance_call = True
            call_name = self.class_name + '.' + func_name
            self.vm_writer.write_push(POINTER, 0)

        self._advance_n_times(1)  # Advance past the '('
        num_params = self.compile_expression_list()
        self._advance_n_times(2)  # Advance past the ');'

        self.vm_writer.write_call(call_name, num_params + instance_call)
        self.vm_writer.write_pop('temp', 0)

    def compile_let(self):
        """Compiles a let statement"""
        self._advance_n_times(1)
        var_name = self._get_next_token()

        array = False
        if self.tokenizer.symbol() == '[':
            # This section will calculate the base pointer of the array plus the index and store it on top of the stack
            array = True
            self._advance_n_times(1)  # Advance past the [
            self.compile_expression()  # Leaves the desired index at the top of the stack
            self.vm_writer.write_push(self.symbol_table.get_pointer_type_from_kind(var_name), self.symbol_table.index_of(var_name))
            self.vm_writer.write_arithmetic(ADD)
            self._advance_n_times(1)  # Advance past the ]

        self._advance_n_times(1)  # Advance past the '='
        self.compile_expression()  # Is responsible for pushing the value to the top of the stack

        if array:
            # This section will store the value we wish to insert into the array into temp.
            # Then it will retrieve the address calculated above and store it in pointer
            # Then it will return the value to the top of the stack and then write it to the array
            self.vm_writer.write_pop(TEMP, 0)
            self.vm_writer.write_pop(POINTER, 1)
            self.vm_writer.write_push(TEMP, 0)
            self.vm_writer.write_pop(THAT, 0)
        else:
            stack_kind = self.symbol_table.get_pointer_type_from_kind(var_name)
            pointer_index = self.symbol_table.index_of(var_name)
            self.vm_writer.write_pop(stack_kind, pointer_index)

        self._advance_n_times(1)  # Advance past the ';'

    def compile_while(self):
        """Compiles a while statement"""
        l1 = self._get_if_label()
        l2 = self._get_if_label()

        self.vm_writer.write_label(l1)
        self._advance_n_times(1)  # Advance past the '('

        self.compile_expression()  # Leaves cond on top of the stack
        self.vm_writer.write_arithmetic(NOT)  # Leaves ~(cond) on top of the stack
        self.vm_writer.write_if(l2)  # Check to see if we should exit the loop or not

        self._advance_n_times(1)  # Advance past the '{'
        self.compile_statements()  # Execute the code in the loop
        self.vm_writer.write_goto(l1)  # Iterate one more time over the loop

        self.vm_writer.write_label(l2)
        self._advance_n_times(1)  # Advance past the '}'

    def compile_return(self):
        """Compiles a return statement"""
        self._advance_n_times(1)  # Advance over the 'return' keyword
        if self.tokenizer.symbol() != ';':  # If there is a return value
            self.compile_expression()  # Leaves the return value on top of the stack
        else:  # If the function returns void
            self.vm_writer.write_push(CONSTANT, 0)
        self.vm_writer.write_return()
        self._advance_n_times(1)  # Advance past the ';'

    def _get_if_label(self) -> str:
        label = 'if_' + str(self.if_counter)
        self.if_counter += 1
        return label

    def compile_string_constant(self, string: str):
        """Accepts a string constant as an argument and write the VM code to compile it"""
        self.vm_writer.write_push(CONSTANT, len(string))
        self.vm_writer.write_call('String.new', 1)
        for char in string:
            self.vm_writer.write_push(CONSTANT, ord(char))
            self.vm_writer.write_call('String.appendChar', 2)

    def compile_if(self):
        """Compiles an if statement, possibly with a trailing else clause"""
        l1 = self._get_if_label()
        l2 = self._get_if_label()

        self._advance_n_times(1)  # Advance past the '('
        self.compile_expression()  # Leaves the condition on top of the stack
        self.vm_writer.write_arithmetic(NOT)  # Leaves ~(cond) on top of the stack
        self.vm_writer.write_if(l1)

        self._advance_n_times(1)  # Advance past the ')' and {
        self.compile_statements()  # Execute the code in the if statement
        self._advance_n_times(1)  # Advance past the '}'

        if self.tokenizer.keyword() == ELSE:
            self.vm_writer.write_goto(l2)

        self.vm_writer.write_label(l1)

        if self.tokenizer.keyword() == ELSE:
            self._advance_n_times(2)  # Advance past the '{'
            self.compile_statements()  # Execute the code in the else statement
            self._advance_n_times(1)  # Advance past the '}'
            self.vm_writer.write_label(l2)

    def compile_expression(self):
        """Compiles an expression"""
        self.compile_term()
        while self.tokenizer.symbol() in OPS.keys():  # todo changed to
            # while to handle expression like x+y+z, check it won't mess
            # anything up
            operator = self._get_next_token()  # binary operator
            self.compile_term()  # Leaves the second operand on top of the stack
            self.vm_writer.write_arithmetic(OPS[operator])

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
            self.compile_string_constant(self._get_next_token())
        elif _token_type == 'int_const':
            self.vm_writer.write_push(CONSTANT, self._get_next_token())
        elif _token_type == 'keyword':
            next_token = self._get_next_token()
            if next_token == 'true':  # place -1 on top of stack
                self.vm_writer.write_push(CONSTANT, 1)
                self.vm_writer.write_arithmetic('neg')
            elif next_token in {'null', 'false'}:
                self.vm_writer.write_push(CONSTANT, 0)
            elif next_token == 'this':
                self.vm_writer.write_push(POINTER, 0)
        elif _token_type == 'identifier':
            _name = self._get_next_token()
            if self.tokenizer.symbol() == '.':  # subroutine call
                self._advance_n_times(1)  # Advance past the '.'
                func_name = self._get_next_token()
                stack_kind = self.symbol_table.get_pointer_type_from_kind(
                    _name)
                if stack_kind:  # This is a method

                    self.vm_writer.write_push(
                        self.symbol_table.get_pointer_type_from_kind(_name),
                        self.symbol_table.index_of(_name))

                self._advance_n_times(1)  # Advance past the '('
                num_args = self.compile_expression_list()  # params
                self._advance_n_times(1)  # Advance past the ')'
                call_name = _name + '.' + func_name

                if not stack_kind:  # function or constructor call (i.e not method)
                    self.vm_writer.write_call(call_name, num_args)
                else:  # a method call of another class
                    call_name = self.symbol_table.type_of(_name) + '.' + func_name
                    self.vm_writer.write_call(call_name, num_args + 1)

            elif self.tokenizer.symbol() == '[':  # array entry
                # Order of operations:
                # 1. Evaluate the expression within the brackets
                # 2. Calculate base_address + resultant of step 1, and store on top of stack
                # 3. Move address to the 'that' section of the 'pointer' segment
                # 4. Push the value in the array onto the top of the stack
                self._advance_n_times(1)  # Advance over the [
                self.compile_expression()
                self.vm_writer.write_push(self.symbol_table.get_pointer_type_from_kind(_name), self.symbol_table.index_of(_name))
                self.vm_writer.write_arithmetic(ADD)
                self.vm_writer.write_pop(POINTER, 1)
                self.vm_writer.write_push(THAT, 0)
                self._advance_n_times(1)  # Advance over the ]
            elif self.tokenizer.symbol() == '(':  # a method of this class
                self._advance_n_times(1)
                num_args = self.compile_expression_list()  # params
                self._advance_n_times(1)  # Advance past the ')'
                call_name = self.class_name + '.' + _name
                self.vm_writer.write_call(call_name, num_args + 1)

            else:
                self.vm_writer.write_push(
                    self.symbol_table.get_pointer_type_from_kind(_name),
                    self.symbol_table.index_of(_name))

        elif _token_type == 'symbol':
            if self.tokenizer.symbol() == '(':
                self._advance_n_times(1)  # Advance past the '('
                self.compile_expression()
                self._advance_n_times(1)  # Advance past the ')'
            else:
                op = self._get_next_token()
                self.compile_term()
                self.vm_writer.write_arithmetic(OPS[op])  # unary op


    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions"""
        num_expressions = 0
        if self.tokenizer.symbol() != ')':  # non-empty list
            self.compile_expression()
            num_expressions += 1
            while self.tokenizer.symbol() == ',':
                self._advance_n_times(1)  # Advance over the comma
                self.compile_expression()
                num_expressions += 1
        return num_expressions
