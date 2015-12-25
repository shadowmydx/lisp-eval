import sys
sys.path.append('../')
from Function import Function
from parsers.Parser import GrammarNode
from parsers.Parser import GrammarTree
__author__ = 'shadowmydx'


def occupy_func(arguments, env):
    pass


def add(arguments, env):
    total = 0
    for item in arguments:
        try:
            total += int(item)
        except:
            raise Exception('you can not add a non-number item')
    return total


def sub(arguments, env):
    return arguments[0] - arguments[1]


def times(arguments, env):
    return arguments[0] * arguments[1]


def divide(arguments, env):
    return arguments[0] / arguments[1]


def bigger(arguments, env):
    return arguments[0] > arguments[1]


def smaller(arguments, env):
    return arguments[0] < arguments[1]


def equal(arguments, env):
    return arguments[0] == arguments[1]


def cons(items, env):
    result = list()
    item_1 = items[0]
    item_2 = items[1]
    result.append(item_1)
    if isinstance(item_2, list):
        result += item_2
    else:
        result.append(item_2)
    return result


def car(target_list, env):
    return target_list[0][0]


def cdr(target_list, env):
    if len(target_list[0]) == 0:
        return None
    return target_list[0][1:]


def dic(env):
    return dict()


def put(args, env):
    target = args[0]
    key = args[1]
    value = args[2]
    target[key] = value
    return target


def get(args, env):
    target = args[0]
    key = args[1]
    if key in target:
        return target[key]
    return None


def delete(args, env):
    target = args[0]
    key = args[1]
    if key in target:
        target.pop(key)
    return target


def define(marks, env):
    env.add_constraint(marks[0], marks[1])
    return marks[1]


def display(target, env):
    print target[0]
    return None


def custom_list(arguments, env):
    result = list()
    for item in arguments:
        result.append(item)
    return result


def custom_lambda(trees, env):
    function = Function()
    function.set_body(trees[1])
    function.set_scope(env)
    args = trees[0]
    args_list = list()
    for arg in args.children:
        if isinstance(arg, GrammarTree):
            raise Exception('arguments should not be a expression.')
        args_list.append(arg.get_value())
    function.set_args(args_list)
    return function


def custom_if(statements, env):
    if statements[0]:
        return statements[1]
    return statements[2]


def custom_not(statements, env):
    return not statements[0]


def custom_and(statements, env):
    return statements[0] and statements[1]


def custom_or(statements, env):
    return statements[0] or statements[1]


def string_add(arguments, env):
    result = ''
    for item in arguments:
        result += item
    return result


def is_null(arguments, env):
    return arguments[0] is None or len(arguments[0]) == 0


if __name__ == '__main__':
    print cons((1, 2), {})
    print type(cons)
