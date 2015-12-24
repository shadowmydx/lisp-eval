__author__ = 'shadowmydx'


class Function:

    def __init__(self):
        self.grammar = None
        self.arguments = None
        self.scope = None

    def set_body(self, grammar):
        self.grammar = grammar

    def set_args(self, arguments):
        self.arguments = arguments

    def get_body(self):
        return self.grammar

    def get_args(self):
        return self.arguments

    def set_scope(self, scope):
        self.scope = scope

    def get_scope(self):
        return self.scope
