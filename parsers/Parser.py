import re
__author__ = 'shadowmydx'


class WordItem:

    def __init__(self, item):
        self.item = item

    def get_type(self):
        return self.item[1]

    def get_value(self):
        return self.item[0]


class WordParser:

    def __init__(self):
        self.space = re.compile(r'\s')
        self.number = re.compile(r'\d+')

    def word_parse(self, content):
        result = list()
        index = 0
        while index < len(content):
            index, single_item = self.next_item(content, index)
            if single_item.get_type() == 'end':
                break
            result.append(single_item)
        return result

    def next_item(self, content, start):
        item = ''
        while start < len(content) and self.space.match(content[start]):
            start += 1
        if start >= len(content):
            return start, WordItem((-1, 'end'))
        if content[start] == '(':
            item = ('(', 'left-bracket')
            item = WordItem(item)
            start += 1
        elif content[start] == ')':
            item = (')', 'right-bracket')
            item = WordItem(item)
            start += 1
        else:
            while start < len(content) and content[start] != ')' and content[start] != '(' \
                    and (not self.space.match(content[start])):
                item += content[start]
                start += 1
            if item.startswith("'"):
                item = (item, 'string')
                item = WordItem(item)
            elif self.number.match(item):
                item = (item, 'number')
                item = WordItem(item)
            else:
                item = (item, 'var')
                item = WordItem(item)
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

    def get_type(self):
        return self.type

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

    def get_callable_child(self):
        return self.children[0]

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

    def parse_one_round(self, item_list, start):
        curr_item = item_list[start]
        if curr_item.get_type() == 'left-bracket':
            return self.generate_grammar_tree(item_list, start + 1)
        else:
            return self.generate_single_node(item_list, start)

    def generate_grammar_tree(self, item_list, start):
        index = start
        result_tree = GrammarTree()
        count_left = 1
        while index < len(item_list) and count_left != 0:
            curr_item = item_list[index]
            if curr_item.get_type() == 'left-bracket':
                index, child_item = self.generate_grammar_tree(item_list, index + 1)
                result_tree.add_child(child_item)
            elif curr_item.get_type() == 'right-bracket':
                count_left -= 1
                index += 1
            else:
                index, node = self.generate_single_node(item_list, index)
                result_tree.add_child(node)
        return index, result_tree

    @staticmethod
    def generate_single_node(item_list, index):
        curr_item = item_list[index]
        node = GrammarNode()
        node.set_type(curr_item.get_type())
        node.set_value(curr_item.get_value())
        return index + 1, node


if __name__ == '__main__':
    parser = WordParser()
    grammar = GrammarParser()
    test = "'1234"
    print parser.word_parse(test)[0].get_type()


