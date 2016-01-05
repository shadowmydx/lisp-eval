import re
__author__ = 'shadowmydx'


def correct_split(cols):
    result = list()
    tmp_str = ''
    index = 0
    while index < len(cols):
        char = cols[index]
        index += 1
        if char == '\'':
            tmp_str += char
            while True:
                try:
                    tmp_str += cols[index]
                    if cols[index] == '\'':
                        index += 1
                        break
                    index += 1
                except IndexError:
                    print "Error : other " + tmp_str
                    break
        elif char == '(':
            start_quote = 1
            tmp_str += char
            while start_quote != 0:
                try:
                    tmp_str += cols[index]
                    if cols[index] == '(':
                        start_quote += 1
                    elif cols[index] == ')':
                        start_quote -= 1
                    index += 1
                except IndexError:
                    print 'ERROR: in quote ' + cols
                    break
        elif char == ',':
            result.append(tmp_str)
            tmp_str = ''
        else:
            tmp_str += char
    result.append(tmp_str)
    return result


def change_statement_value(statement, column_name, new_value):
    pattern = re.compile(r"INSERT(\s*)INTO(\s*)(?P<table>.*?)(\s*)\((?P<cols>.*?)\)(\s*)"
                         r"VALUES(\s*)\((?P<vals>.*?)\)(\s*)$", re.DOTALL)
    m = pattern.search(statement)
    if m:
        cols_val = correct_split(m.group('vals'))
        cols_name = [item.upper().strip() for item in m.group('cols').split(',')]
        start = -1
        for index in xrange(len(cols_name)):
            column = cols_name[index]
            if column == column_name:
                start = index
        if start != -1:
            cols_val[start] = new_value
            cols_val = ','.join(cols_val)
            statement = statement.replace(m.group('vals'), cols_val)
    return statement


def get_statement_value(statement, column_name):
    pattern = re.compile(r"INSERT(\s*)INTO(\s*)(?P<table>.*?)(\s*)\((?P<cols>.*?)\)(\s*)"
                         r"VALUES(\s*)\((?P<vals>.*?)\)(\s*)$", re.DOTALL)
    m = pattern.search(statement)
    if m:
        cols_val = correct_split(m.group('vals'))
        cols_name = [item.upper().strip() for item in m.group('cols').split(',')]
        start = -1
        for index in xrange(len(cols_name)):
            column = cols_name[index]
            if column == column_name:
                start = index
        if start != -1:
            return cols_val[start]
    return None


def open_file(arguments, env):
    f = open(arguments[0], 'r')
    result = f.read()
    f.close()
    return result


def split_sql(arguments, env):
    content = arguments[0]

    def jump_next_char(begin, target):
        index_inside = begin
        while content[index_inside] != target:
            index_inside += 1
        return index_inside
    result = list()
    index = 0
    start = 0
    while index < len(content):
        if content[index] == '"':
            index = jump_next_char(index + 1, '"')
        elif content[index] == '\'':
            index = jump_next_char(index + 1, '\'')
        elif content[index] == ';':
            result.append(content[start:index])
            start = index + 1
        index += 1
    return result


def set_by_column(arguments, env):
    statement = arguments[0]
    column_name = arguments[1]
    column_value = arguments[2]
    return change_statement_value(statement, column_name, column_value)


def get_by_column(arguments, env):
    statement = arguments[0]
    column_name = arguments[1]
    return get_statement_value(statement, column_name)


def write_file(arguments, env):
    path = arguments[0]
    content = arguments[1]
    content = ';'.join(content) + ';'
    f = open(path, 'w')
    f.write(content + '\n/')
    f.close()
    return None


if __name__ == '__main__':
    test = '''
INSERT INTO ALM_DEFECT (d_id, d_name, d_state, d_project_id, d_desc, d_owner_id, d_submit_by, d_critical_lv, d_release_id, d_story_id, d_iteration_id, formatted_id, d_custom_field_value, D_TESTCASE_ID) VALUES ('18618341136','Sample Defect',1,'18489072769',v_desc,'11792998249','11792998249',0,'18492178020','18591784384',null,'DE1',v_custom_field_value,'18618339840')
    '''
    state = get_by_column((test, 'D_ID'), None)
    print state
