import itertools


def flatten(nested_list: list[list]):
    """ Flattens nested list to single list """
    return list(itertools.chain(*nested_list))


def read_clear_line(f):
    """ Reads line from a file without \n at the end """
    return f.readline().rstrip('\n')


def read_until(f, ending='.') -> list[str]:
    """ Reads lines from a file until meets the given ending.
     Returns all those lines concatenated.
     """
    line = read_clear_line(f)
    lines: list[str] = [line]
    while line and not line.endswith(ending):
        line = read_clear_line(f)
        lines.append(line)
    return lines


def string_list_to_list(s) -> list[str]:
    """ Converts string in list format to real list.
     E.g.:
        '[i1,i2,i3].'   ->  ['i1', 'i2', 'i3']
        '[[i1,i2,i3],'  ->  ['i1', 'i2', 'i3']
     """
    return s.strip('[],.()').split(',')


def tuplize(items):
    return [(i, i) for i in items]


def clone_django_object(obj):
    obj.pk = None
    obj.save()
    return obj


def is_superset(superset, subset):
    return all(item in superset for item in subset)


def remove_subset(superset, subset):
    assert is_superset(superset, subset)
    for item in subset:
        superset.remove(item)
    return superset


def mean(l):
    return sum(l) / len(l)


def num_to_booleans(num, length) -> list[bool]:
    return [
        bool(eval(bit_str))
        for bit_str in format(num, f'0{length}b')
    ]
