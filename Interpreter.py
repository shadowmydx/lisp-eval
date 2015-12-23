from parsers.Parser import GrammarParser
from parsers.Parser import WordParser
from parsers.Parser import GrammarNode
from basic.Operation import *
from parsers.Parser import GrammarTree
from runtime.Environment import Environment
__author__ = 'shadowmydx'


def setup_global_env():
    env = Environment()
    env.add_constraint('+', add)
    env.add_constraint('cons', cons)
    env.add_constraint('car', car)
    env.add_constraint('cdr', cdr)
    env.add_constraint('lambda', custom_lambda)
    env.add_constraint('define', define)
    # env.add_constraint('+', (add, 'build-in'))
    # env.add_constraint('cons', (cons, 'build-in'))
    # env.add_constraint('car', (car, 'build-in'))
    # env.add_constraint('cdr', (cdr, 'build-in'))
    # env.add_constraint('lambda', (custom_lambda, 'build-in'))
    return env


def eval_expression(grammar_node, env):
    def get_args(grammar_tree):
        result = list()
        for ptr in xrange(1, len(grammar_tree.children)):
            child = grammar_tree.children[ptr]
            eval_item = eval_expression(child, env)
            result.append(eval_item)
        return result

    def execute_func(func, exe_args):
        new_env = Environment()
        new_env.set_father_scope(env)
        for index in xrange(len(func.get_args())):
            arg = func.get_args()[index]
            new_env.add_constraint(arg, exe_args[index])
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

if __name__ == '__main__':
    global_env = setup_global_env()
    word_parser = WordParser()
    grammar_parser = GrammarParser()
    # test = '(cdr (cons (+ 1 (+ 2 3) 4 (+ 3 (+ 1 2))) 3))'
    # item_list = word_parser.word_parse(test)
    # next, node = grammar_parser.parse_one_round(item_list, 0)
    # print eval_expression(node, global_env)

    test = '((lambda (x y z) (+ x y z)) 1 2 3)'
    item_list = word_parser.word_parse(test)
    next_num, node = grammar_parser.parse_one_round(item_list, 0)
    print eval_expression(node, global_env)

    test = '(define x 2) x'
    item_list = word_parser.word_parse(test)
    next_num, node = grammar_parser.parse_one_round(item_list, 0)
    print eval_expression(node, global_env)
    next_num, node = grammar_parser.parse_one_round(item_list, next_num)
    print eval_expression(node, global_env)
