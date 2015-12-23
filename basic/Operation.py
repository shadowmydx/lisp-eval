import sys
sys.path.append('../')
from Function import Function
from parsers.Parser import GrammarNode
from parsers.Parser import GrammarTree
__author__ = 'shadowmydx'


def add(arguments, env):
    total = 0
    for item in arguments:
        try:
            total += int(item)
        except:
            raise Exception('you can not add a non-number item')
    return total


def bigger(arguments, env):
    return arguments[0] > arguments[1]


def smaller(arguments, env):
    return arguments[0] < arguments[1]


def equal(arguments, env):
    return arguments[0] == arguments[1]


def cons(items, env):
    result = list()
    result.append(items[0])
    result.append(items[1])
    return result


def car(target_list, env):
    return target_list[0][0]


def cdr(target_list, env):
    return target_list[0][1:]


def define(marks, env):
    env.add_constraint(marks[0], marks[1])
    return marks[1]


def custom_lambda(trees, env):
    function = Function()
    function.set_body(trees[1])
    args = trees[0]
    args_list = list()
    for arg in args.children:
        if isinstance(arg, GrammarTree):
            raise Exception('arguments should not be a expression.')
        args_list.append(arg.get_value())
    function.set_args(args_list)
    return function


if __name__ == '__main__':
    print cons((1, 2), {})
    print type(cons)
