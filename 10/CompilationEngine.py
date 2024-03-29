from lxml import etree as et
NEWLINE = '\n'
OPS = {'+', '-', '*', '/', '&', '|', '<', '>', '='}


class CompilationEngine:
    """
    Effects the actual compilation output.
    It receives it input from the JackTokenizer and emits
    its parsed structure into an output file
    """

    def __init__(self, tokenizer_object, output_file):
        self.tokenizer = tokenizer_object
        self.output_file = output_file
        self.cur_node = None
        self.root = None
        self.compile_class()
        # et.indent(self.root, space='  ')
        print(str(et.tostring(self.root, pretty_print=False), 'UTF-8'), file=self.output_file)

    def compile_class(self):
        """Compiles a complete class"""
        if not self.tokenizer.has_more_tokens():  # empty file (necessary?)
            return

        self.tokenizer.advance()
        self.cur_node = et.Element("class")
        self.cur_node.text = '\n'
        self.root = self.cur_node
        self._add_xml_node("keyword", "class")
        self.tokenizer.advance()
        self._add_identifier()
        self._add_symbol()

        while self.tokenizer.keyword() in {"static", "field"}:
            self.compile_class_var_dec()

        while self.tokenizer.keyword() in {"constructor", "function",
                                           "method"}:
            self.compile_subroutine()

        self._add_xml_node("symbol", "}")

    def _add_xml_node(self, tag, text, descend=False):
        """
        Adds an xml node to the tree as a child of current node.
        :param tag:
        :param text:
        :param descend: if True, changes current node to child.
        """
        new_node = et.SubElement(self.cur_node, tag)
        new_node.tail = '\n'
        if descend:
            new_node.text = '\n'
            self.cur_node = new_node
        else:
            new_node.text = text

    def _add_keyword(self):
        self._add_xml_node("keyword", self.tokenizer.keyword())
        self.tokenizer.advance()

    def _add_identifier(self):
        self._add_xml_node("identifier", self.tokenizer.identifier())
        self.tokenizer.advance()

    def _add_symbol(self):
        self._add_xml_node("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

    def compile_class_var_dec(self):
        """Compiles a static declaration or a field declaration"""
        self._add_xml_node("classVarDec", "", descend=True)

        self._add_keyword()  # static or field

        if self.tokenizer.token_type() == "keyword":  # var is built-in type
            self._add_keyword()
        else:  # var is user-defined class
            self._add_identifier()

        self._add_identifier()  # variable name

        while self.tokenizer.symbol() == ',':  # multiple varDecs in one line
            self._add_symbol()
            self._add_identifier()

        self._add_symbol()  # add ';'
        self.cur_node = self.cur_node.getparent()

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor"""
        self._add_xml_node('subroutineDec', '', descend=True)
        self._add_keyword()  # routine type (constructor, function, method)

        if self.tokenizer.token_type() == "keyword":  # routine returns built-in
            self._add_keyword()  # or void
        else:  # routine returns user-defined class
            self._add_identifier()

        self._add_identifier()  # routine name
        self._add_symbol()  # '('
        self.compile_parameter_list()
        self._add_symbol()  # ')'

        self._add_xml_node('subroutineBody', '', descend=True)
        self._add_symbol()  # '{'
        while self.tokenizer.keyword() == "var":
            self.compile_var_dec()
        self.compile_statements()
        self._add_symbol()  # '}'
        self.cur_node = self.cur_node.getparent()

        self.cur_node = self.cur_node.getparent()

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing '()'"""
        self._add_xml_node("parameterList", "", descend=True)

        if self.tokenizer.symbol() == ')':
            self.cur_node.text = '\n'
        while self.tokenizer.symbol() != ')':
            if self.tokenizer.token_type() == "keyword":  # arg is built-in type
                self._add_keyword()
            else:  # arg is user-defined class
                self._add_identifier()
            self._add_identifier()  # arg name
            if self.tokenizer.symbol() == ',':
                self._add_symbol()

        self.cur_node = self.cur_node.getparent()

    def compile_var_dec(self):
        """Compiles a var declaration"""
        self._add_xml_node("varDec", "", descend=True)

        self._add_keyword()  # 'var'

        if self.tokenizer.token_type() == "keyword":  # var is built-in type
            self._add_keyword()
        else:  # var is user-defined class
            self._add_identifier()

        self._add_identifier()  # variable name

        while self.tokenizer.symbol() == ',':  # multiple varDecs in one line
            self._add_symbol()
            self._add_identifier()

        self._add_symbol()  # add ';'
        self.cur_node = self.cur_node.getparent()

    def compile_statements(self):
        """Compiles a sequence of statements, not including the enclosing '()'"""
        self._add_xml_node("statements", "", descend=True)

        statement_dict = {
            "do": self.compile_do,
            "let": self.compile_let,
            "while": self.compile_while,
            "return": self.compile_return,
            "if": self.compile_if
        }
        while self.tokenizer.keyword() in statement_dict:
            statement_dict[self.tokenizer.keyword()]()

        self.cur_node = self.cur_node.getparent()

    def compile_do(self):
        """Compiles a do statements"""
        self._add_xml_node("doStatement", "", descend=True)
        self._add_keyword()  # "do"
        self._add_identifier()  # name of routine, class, or var

        if self.tokenizer.symbol() == '.':  # was class or var
            self._add_symbol()  # '.'
            self._add_identifier()  # name of routine

        self._add_symbol()  # '('
        self.compile_expression_list()
        self._add_symbol()  # ')'
        self._add_symbol()  # ';'

        self.cur_node = self.cur_node.getparent()

    def compile_let(self):
        """Compiles a let statement"""
        self._add_xml_node("letStatement", "", descend=True)

        self._add_keyword()  # "let"
        self._add_identifier()  # var name

        if self.tokenizer.symbol() == '[':  # array index
            self._add_symbol()  # '['
            self.compile_expression()
            self._add_symbol()  # ']'

        self._add_symbol()  # '='
        self.compile_expression()
        self._add_symbol()  # ';'

        self.cur_node = self.cur_node.getparent()

    def compile_while(self):
        """Compiles a while statement"""
        self._add_xml_node("whileStatement", "", descend=True)

        self._add_keyword()  # "while"
        self._add_symbol()  # '('
        self.compile_expression()
        self._add_symbol()  # ')'
        self._add_symbol()  # '{'
        self.compile_statements()
        self._add_symbol()  # '}'

        self.cur_node = self.cur_node.getparent()

    def compile_return(self):
        """Compiles a return statement"""
        self._add_xml_node("returnStatement", "", descend=True)

        self._add_keyword()  # "return"
        if not self.tokenizer.symbol() == ';':
            self.compile_expression()
        self._add_symbol()  # ';'

        self.cur_node = self.cur_node.getparent()

    def compile_if(self):
        """Compiles an if statement, possibly with a trailing else clause"""
        self._add_xml_node("ifStatement", "", descend=True)

        self._add_keyword()  # "if"
        self._add_symbol()  # '('
        self.compile_expression()
        self._add_symbol()  # ')'
        self._add_symbol()  # '{'
        self.compile_statements()
        self._add_symbol()  # '}'

        if self.tokenizer.keyword() == "else":
            self._add_keyword()  # "else"
            self._add_symbol()  # '{'
            self.compile_statements()
            self._add_symbol()  # '}'

        self.cur_node = self.cur_node.getparent()

    def compile_expression(self):
        """Compiles an expression"""
        self._add_xml_node("expression", "", descend=True)

        self.compile_term()
        if self.tokenizer.symbol() in OPS:
            self._add_symbol()  # binary operator
            self.compile_term()

        self.cur_node = self.cur_node.getparent()

    def compile_term(self):
        """
        Compiles a term.
        If the current token is an identifier, the routine must distinguish between
        a variable, an array entry, and a subroutine call.
        A single look ahead token, which may be '[', '(', or '.' suffices
        to distinguish between the three possibilities.
        Any other token is not part of this term and should not be advanced over.
        """
        self._add_xml_node('term', '', descend=True)

        _token_type = self.tokenizer.token_type()
        if _token_type == 'string_const':
            self._add_xml_node('stringConstant', self.tokenizer.string_val())
            self.tokenizer.advance()
        elif _token_type == 'int_const':
            self._add_xml_node('integerConstant', self.tokenizer.int_val())
            self.tokenizer.advance()
        elif _token_type == 'keyword':
            self._add_keyword()
        elif _token_type == 'identifier':
            self._add_identifier()
            if self.tokenizer.symbol() == '.':  # subroutine call
                self._add_symbol()  # '.'
                self._add_identifier()  # func name
                self._add_symbol()  # '('
                self.compile_expression_list()  # params
                self._add_symbol()  # ')'
            elif self.tokenizer.symbol() == '[':  # array entry
                self._add_symbol()  # '['
                self.compile_expression()
                self._add_symbol()  # ']'
        elif _token_type == 'symbol':
            if self.tokenizer.symbol() == '(':
                self._add_symbol()  # '('
                self.compile_expression()
                self._add_symbol()  # ')'
            else:
                self._add_symbol()  # unary op
                self.compile_term()

        self.cur_node = self.cur_node.getparent()

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions"""
        self._add_xml_node('expressionList', '', descend=True)
        if self.tokenizer.symbol() != ')':  # non-empty list
            self.compile_expression()
            while self.tokenizer.symbol() == ',':
                self._add_symbol()  # ','
                self.compile_expression()
        else:
            self.cur_node.text = '\n'
        self.cur_node = self.cur_node.getparent()
