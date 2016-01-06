__author__ = 'shadowmydx'


class LazyFunction:

    def __init__(self):
        self.executable = None
        self.environment = None

    def set_executable(self, executable):
        self.executable = executable

    def set_environment(self, environment):
        self.environment = environment

    def get_executable(self):
        return self.executable

    def get_environment(self):
        return self.environment
