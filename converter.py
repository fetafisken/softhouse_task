#!/usr/bin/env python3
import sys

# newl = '\r\n'
newl = '\n'
blnk = '    '
lines = None
index = 0


def s(depth):
    """ Simple indent function. """

    return blnk * depth


def step_back():
    """ Walks back when gone to far. """

    global index
    index -= 1


def next_line():
    """ Walks over the input lines. """

    global index
    if index < len(lines):
        line = lines[index].replace(newl, '')
        index += 1
        return line.split('|')
    return None


def call(func, depth, entry):
    if len(entry) > 3:
        return func(depth, entry[1], entry[2], entry[3])
    elif len(entry) > 2:
        return func(depth, entry[1], entry[2])
    elif len(entry) > 1:
        return func(depth, entry[1])

    return ''


def dis_people():
    """ Used to disclose the content under people. Can only be P. """

    ret = '<people>' + newl
    while True:
        entry = next_line()
        if entry is not None:
            if entry[0] == 'P':
                ret += int_p(1, entry[1], entry[2])
                continue
        break

    ret += '<people>' + newl
    return ret


def dis_p(depth):
    """ Used to disclose the content under P. Can be F, T, A. """

    entry = next_line()
    if entry is not None:
        if entry[0] == 'F':
            return call(int_f, depth, entry)

        elif entry[0] == 'T':
            return call(int_t, depth, entry)

        elif entry[0] == 'A':
            return call(int_a, depth, entry)

    step_back()
    return ''


def dis_f(depth):
    """ Used to disclose the content under F. Can be T, A. """

    entry = next_line()
    if entry is not None:
        if entry[0] == 'T':
            return call(int_t, depth, entry)

        elif entry[0] == 'A':
            return call(int_a, depth, entry)

    step_back()
    return ''


def int_p(depth, fname=None, lname=None):
    """ Interprets a person entry. Can include multiple F, T, A:s. """

    ret = s(depth) + '<person>' + newl
    if fname:
        ret += s(depth) + blnk + '<firstname>' + fname + '</firstname>' + newl
    if lname:
        ret += s(depth) + blnk + '<lastname>' + lname + '</lastname>' + newl

    x = None
    while x != '':
        x = dis_p(depth + 1)
        ret += x

    ret += s(depth) + '</person>' + newl
    return ret


def int_t(depth, mobile=None, number=None):
    """ Interprets a phone entry. """

    ret = s(depth) + '<phone>' + newl
    if mobile:
        ret += s(depth + 1) + '<mobile>' + mobile + '</mobile>' + newl
    if number:
        ret += s(depth + 1) + '<number>' + number + '</number>' + newl

    ret += s(depth) + '</phone>' + newl
    return ret


def int_a(depth, street=None, city=None, zipcode=None):
    """ Interprets an address entry. """

    ret = s(depth) + '<address>' + newl
    if street:
        ret += s(depth + 1) + '<street>' + street + '</street>' + newl
    if city:
        ret += s(depth + 1) + '<city>' + city + '</city>' + newl
    if zipcode:
        ret += s(depth + 1) + '<zipcode>' + zipcode + '</zipcode>' + newl

    ret += s(depth) + '</address>' + newl
    return ret


def int_f(depth, name=None, born=None):
    """ Interprets a family entry. """

    ret = s(depth) + '<family>' + newl
    if name:
        ret += s(depth + 1) + '<name>' + name + '</name>' + newl
    if born:
        ret += s(depth + 1) + '<born>' + born + '</born>' + newl

    ret += dis_f(depth + 1)
    ret += s(depth) + '</family>' + newl
    return ret


def main():
    global lines
    lines = None
    src = 'source.txt'
    dst = 'output.txt'

    argc = len(sys.argv)
    if argc >= 2:
        src = sys.argv[1]
    if argc == 3:
        dst = sys.argv[2]
    if argc > 3:
        print ('Too many arguments. python converter.py [src [dst]]')

    with open(src, 'r') as source:
        lines = source.readlines()

    out = dis_people()

    with open(dst, 'w') as output:
        output.write(out)


if __name__ == '__main__':
    main()
