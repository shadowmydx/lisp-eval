__author__ = 'shadowmydx'


class Environment:

    def __init__(self):
        self.scope = dict()
        self.scope['father'] = None  # father scope

    def set_father_scope(self, scope):
        self.scope['father'] = scope

    def add_constraint(self, bind, item):
        self.scope[bind] = item

    def search_bind(self, bind):
        if bind in self.scope:
            return self.scope[bind]
        if self.scope['father'] is not None:
            return self.scope['father'].search_bind(bind)
        return None
