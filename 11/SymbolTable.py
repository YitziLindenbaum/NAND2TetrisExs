STATIC = 'static'
FIELD = 'field'
ARG = 'arg'
VAR = 'var'
NONE = 'none'
THIS = 'this'
KIND = {STATIC, FIELD, ARG, VAR}


class SymbolTable:

    def __init__(self):
        # Each dictionary is of the form {key=name: values=(type, kind, index)}
        self.class_scope = dict()
        self.subroutine_scope = dict()
        self.static_index: int = 0
        self.field_index: int = 0
        self.arg_index: int = 0
        self.var_index: int = 0

    def start_subroutine(self):
        """
        Starts a new subroutine scope (i.e resets the subroutine's symbol table)
        """
        self.subroutine_scope = dict()
        self.arg_index = 0
        self.var_index = 0

    def define(self, _name: str, _type: str, _kind: str):
        """
        Defines a new identifier of a given name, type, and kind and assigns it a running index.
        STATIC and FIELD identifiers have a class scope while ARG and VAR identifiers have a subroutine scope.
        Args:
            _name:
            _type:
            _kind: Can be any of the strings in KIND above
        """
        if _kind == ARG:
            self.subroutine_scope[_name] = (_type, _kind, self.arg_index)
            self.arg_index += 1
        elif _kind == VAR:
            self.subroutine_scope[_name] = (_type, _kind, self.var_index)
            self.var_index += 1
        elif _kind == FIELD:
            self.class_scope[_name] = (_type, _kind, self.field_index)
            self.field_index += 1
        elif _kind == STATIC:
            self.class_scope[_name] = (_type, _kind, self.static_index)
            self.static_index += 1

    def var_count(self, _kind: str) -> int:
        """
        Returns the number of variables of the given kind already defined in the current scope
        Args:
            _kind: Can be any of the strings in the KIND above
        """
        if _kind == ARG:
            return self.arg_index
        elif _kind == VAR:
            return self.var_index
        elif _kind == FIELD:
            return self.field_index
        elif _kind == STATIC:
            return self.static_index

    def kind_of(self, _name: str) -> str:
        """
        Returns the kind of the named identifier in the current scope.
        If the identifier is unknown in the current scope, returns NONE
        Return: One of the strings listed in KIND or NONE
        """
        if _name in self.subroutine_scope:
            return self.subroutine_scope[_name][1]
        elif _name in self.class_scope:
            return self.class_scope[_name][1]
        else:
            return NONE

    def type_of(self, _name: str) -> str:
        """
        Returns the type of the named identifier in the current scope
        """
        if _name in self.subroutine_scope:
            return self.subroutine_scope[_name][0]
        elif _name in self.class_scope:
            return self.class_scope[_name][0]

    def index_of(self, _name: str) -> int:
        """
        Returns the index assigned to the named identifier
        """
        if _name in self.subroutine_scope:
            return self.subroutine_scope[_name][2]
        elif _name in self.class_scope:
            return self.class_scope[_name][2]

    def get_pointer_type_from_kind(self, _name: str):
        """
        Takes in the name of a variable and returns the type to be used in the stack call.
        For instance, arg->argument and field->this
        """
        _kind = self.kind_of(_name)
        if _kind == FIELD:
            return THIS
        elif _kind == ARG:
            return 'argument'
        elif _kind == VAR:
            return 'local'
        elif _kind == STATIC:
            return STATIC
        else:
            return None
