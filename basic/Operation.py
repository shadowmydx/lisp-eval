__author__ = 'shadowmydx'


def add(arguments):
    total = 0
    for item in arguments:
        total += int(item)
    return total


def cons(items):
    result = list()
    result.append(items[0])
    result.append(items[1])
    return result


def car(target_list):
    return target_list[0]


def cdr(target_list):
    return target_list[1:]


if __name__ == '__main__':
    print cons((1, 2))
