NEWLINE = '\n'


class CompilationEngine:
    """
    Effects the actual compilation output.
    It receives it input from the JackTokenizer and emits
    its parsed structure into an output file
    """

    def __init__(self, tokenizer_object, output_file):
        self.tokenizer = tokenizer_object
        self.output_file = output_file

    def compile_class(self):
        """Compiles a complete class"""
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            # self.out_file.write(code)
            # self.out_file.write(NEWLINE)

    def compile_class_var_dec(self):
        """Compiles a static declaration or a field declaration"""
        pass

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor"""
        pass

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing '()'"""
        pass

    def compile_var_dec(self):
        """Compiles a var declaration"""
        pass

    def compile_statements(self):
        """Compiles a sequence of statements, not including the enclosing '()'"""
        pass

    def compile_do(self):
        """Compiles a do statements"""
        pass

    def compile_let(self):
        """Compiles a let statement"""
        pass

    def compile_while(self):
        """Compiles a while statement"""
        pass

    def compile_return(self):
        """Compiles a return statement"""
        pass

    def compile_if(self):
        """Compiles an if statement, possibly with a trailing else clause"""
        pass

    def compile_expression(self):
        """Compiles an expression"""
        pass

    def compile_term(self):
        """
        Compiles a term.
        If the current token is an identifier, the routine must distinguish between
        a variable, an array entry, and a subroutine call.
        A single look ahead token, which may be '[', '(', or '.' suffices
        to distinguish between the three possibilities.
        Any other token is not part of this term and should not be advanced over.
        """
        pass

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-seperated list of expressions"""
        pass
