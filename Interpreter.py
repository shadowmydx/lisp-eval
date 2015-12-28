from parsers.Parser import GrammarParser
from parsers.Parser import WordParser
from parsers.Parser import GrammarNode
from basic.Operation import *
from basic.Plugin import *
from parsers.Parser import GrammarTree
from runtime.Environment import Environment
import sys
__author__ = 'shadowmydx'


def setup_global_env():
    env = Environment()
    env.add_constraint('nil', None)
    env.add_constraint('+', add)
    env.add_constraint('-', sub)
    env.add_constraint('*', times)
    env.add_constraint('/', divide)
    env.add_constraint('>', bigger)
    env.add_constraint('=', equal)
    env.add_constraint('<', smaller)
    env.add_constraint('cons', cons)
    env.add_constraint('car', car)
    env.add_constraint('cdr', cdr)
    env.add_constraint('if', custom_if)
    env.add_constraint('lambda', custom_lambda)
    env.add_constraint('or', custom_or)
    env.add_constraint('and', custom_and)
    env.add_constraint('not', custom_not)
    env.add_constraint('define', define)
    env.add_constraint('begin', occupy_func)
    env.add_constraint('display', display)
    env.add_constraint('quote', occupy_func)
    env.add_constraint('get-quote', occupy_func)
    env.add_constraint('get-space', occupy_func)
    env.add_constraint('concat', string_add)
    env.add_constraint('build-dict', dic)
    env.add_constraint('add-dict-item', put)
    env.add_constraint('get-dict-item', get)
    env.add_constraint('delete-dict-item', delete)
    env.add_constraint('null?', is_null)
    env.add_constraint('list', custom_list)
    env.add_constraint('map', occupy_func)
    # env.add_constraint('+', (add, 'build-in'))
    # env.add_constraint('cons', (cons, 'build-in'))
    # env.add_constraint('car', (car, 'build-in'))
    # env.add_constraint('cdr', (cdr, 'build-in'))
    # env.add_constraint('lambda', (custom_lambda, 'build-in'))
    return env


def eval_expression(grammar_node, env):
    def get_args_string(grammar_tree):
        result = ''
        for ptr in xrange(1, len(grammar_tree.children)):
            child = grammar_tree.children[ptr]
            result += child.get_value()
        return result

    def get_args(grammar_tree):
        result = list()
        for ptr in xrange(1, len(grammar_tree.children)):
            child = grammar_tree.children[ptr]
            eval_item = eval_expression(child, env)
            result.append(eval_item)
        return result

    def execute_func(func, exe_args):
        new_env = Environment()
        new_env.set_father_scope(func.get_scope())
        for index in xrange(len(func.get_args())):
            arg = func.get_args()[index]
            try:
                new_env.add_constraint(arg, exe_args[index])
            except IndexError:
                print exe_args, func.get_args()
                raise IndexError
        return eval_expression(func.get_body(), new_env)

    if isinstance(grammar_node, GrammarTree):
        oper_ptr = grammar_node.get_callable_child()
        if not isinstance(oper_ptr, GrammarTree):
            oper = env.search_bind(oper_ptr.get_value())
            if callable(oper):
                if oper_ptr.get_value() == 'lambda':
                    return oper(tuple([grammar_node.children[1], grammar_node.children[2]]), env)
                elif oper_ptr.get_value() == 'define':
                    arg_1 = grammar_node.children[1].get_value()
                    arg_2 = eval_expression(grammar_node.children[2], env)
                    return oper(tuple([arg_1, arg_2]), env)
                elif oper_ptr.get_value() == 'if':
                    condition = eval_expression(grammar_node.children[1], env)
                    expression = oper(tuple([condition, grammar_node.children[2], grammar_node.children[3]]), env)
                    return eval_expression(expression, env)
                elif oper_ptr.get_value() == 'begin':
                    args = get_args(grammar_node)
                    return args[-1]
                elif oper_ptr.get_value() == 'quote':
                    return get_args_string(grammar_node)
                elif oper_ptr.get_value() == 'get-space':
                    return ' '
                elif oper_ptr.get_value() == 'build-dict':
                    return oper(env)
                elif oper_ptr.get_value() == 'get-quote':
                    return '\''
                elif oper_ptr.get_value() == 'map':
                    args = get_args(grammar_node)
                    func = args[0]
                    array = args[1]
                    for index in xrange(len(array)):
                        array[index] = execute_func(func, [array[index]])
                    return array
                args = get_args(grammar_node)
                return oper(tuple(args), env)
            elif isinstance(oper, Function):
                args = get_args(grammar_node)
                return execute_func(oper, args)
        elif isinstance(oper_ptr, GrammarTree):
            # lambda function execute.
            function = eval_expression(oper_ptr, env)
            args = get_args(grammar_node)
            return execute_func(function, args)

    elif isinstance(grammar_node, GrammarNode):
        if grammar_node.get_type() == 'number':
            return int(grammar_node.get_value())
        elif grammar_node.get_type() == 'string':
            return str(grammar_node.get_value()[1:])
        elif grammar_node.get_type() == 'var':
            bind_value = env.search_bind(grammar_node.get_value())
            return bind_value


def setup_plugin(env):
    env.add_constraint('write-file', write_file)
    env.add_constraint('get-by-column', get_by_column)
    env.add_constraint('set-by-column', set_by_column)
    env.add_constraint('split-sql', split_sql)
    env.add_constraint('open-file', open_file)
    env.add_constraint('build-error-dict', build_error_dict)


def interpreter(statement):
    global_env = setup_global_env()
    setup_plugin(global_env)
    global_env.set_father_scope(None)
    word_parser = WordParser()
    grammar_parser = GrammarParser()
    item_list = word_parser.word_parse(statement)
    next_num = 0
    while next_num < len(item_list):
        next_num, node = grammar_parser.parse_one_round(item_list, next_num)
        print eval_expression(node, global_env)


def interpreter_file(path):
    f = open(path, 'r')
    statement = f.read()
    f.close()
    interpreter(statement)


if __name__ == '__main__':
    sys.setrecursionlimit(2000)
#     test = '''
# (define my-cons
#     (lambda (x y)
#         (lambda (m)
#             (m x y))))
# (define my-car
#     (lambda (z)
#         (z (lambda (x y)
#              y))))
# (my-car (my-cons 1 2))
#     '''
#     interpreter(test)
#     test = '''
# (concat (get-quote) '16618463666 (get-quote))
#     '''
#     interpreter(test)
    test = '''
    ((lambda (x)
        (+ x 1)) 1)
    '''
    # interpreter(test)
    test = '''
(define N/A
    (concat (get-quote) 'N/A (get-quote)))
    '''
    # interpreter(test)

    interpreter_file('./test.lisp')



