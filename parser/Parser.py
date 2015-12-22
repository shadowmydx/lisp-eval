import re
__author__ = 'shadowmydx'


class WordParser:

    def __init__(self):
        self.space = re.compile(r'\s')
        self.number = re.compile(r'\d+')

    def word_parse(self, content):
        result = list()
        index = 0
        while index != len(content):
            index, single_item = self.next_item(content, index)
            if single_item[1] == 'end':
                break
            result.append(single_item)
        return result

    def next_item(self, content, start):
        item = ''
        while start < len(content) and self.space.match(content[start]):
            start += 1
        if start >= len(content):
            return -1, 'end'
        if content[start] == '(':
            item = ('(', 'left-bracket')
            start += 1
        elif content[start] == ')':
            item = (')', 'right-bracket')
            start += 1
        else:
            while content[start] != ')' and content[start] != '(' and (not self.space.match(content[start])):
                item += content[start]
                start += 1
            if self.number.match(item):
                item = (item, 'number')
            else:
                item = (item, 'var')
        return start, item


class GrammarNode:

    def __init__(self):
        self.type = None
        self.value = None

    def set_type(self, cus_type):
        self.type = cus_type

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def print_value(self, spaces):
        spaces = ''.join([' ' for i in xrange(spaces)])
        return spaces + ', '.join([str(self.value), str(self.type)])


# 1st child has to be callable
class GrammarTree(GrammarNode):

    def __init__(self):
        GrammarNode.__init__(self)
        self.children = None

    def add_child(self, child):
        if self.children is None:
            self.children = list()
        self.children.append(child)

    def print_value(self, spaces):
        number = spaces
        spaces = ''.join([' ' for i in xrange(spaces)])
        result = spaces + 'node\n'
        for item in self.children:
            result += spaces + item.print_value(number + 1) + '\n'
        return result


class GrammarParser:

    def __init__(self):
        pass

    def generate_grammar_tree(self, item_list, start):
        index = start
        result_tree = GrammarTree()
        count_left = 1
        while index < len(item_list) and count_left != 0:
            curr_item = item_list[index]
            if curr_item[1] == 'left-bracket':
                count_left += 1
                index, child_item = self.generate_grammar_tree(item_list, index + 1)
                result_tree.add_child(child_item)
            elif curr_item[1] == 'right-bracket':
                count_left -= 1
                index += 1
            else:
                node = GrammarNode()
                node.set_type(curr_item[1])
                node.set_value(curr_item[0])
                result_tree.add_child(node)
                index += 1
        return index, result_tree

if __name__ == '__main__':
    parser = WordParser()
    grammar = GrammarParser()
    test = '(cons (+ 1 (+ 3 4)) (cons 1 2))'
    print test
    index, tree = grammar.generate_grammar_tree(parser.word_parse(test), 0)
    print tree.print_value(0)


