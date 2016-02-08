#!/usr/bin/env python
"""
Flatten JSON into something more digestible by shells (Bash, etc.)
"""
import fileinput
import json


if __name__ == '__main__':
    content = json.loads(''.join(fileinput.input()))

    def walk(path, item):
        if isinstance(item, list):
            for i in range(len(item)):
                path.append('%d' % i)
                walk(path, item[i])
                path.pop()
        elif isinstance(item, dict):
            for key in item.keys():
                path.append('%s' % key)
                walk(path, item[key])
                path.pop()
        else:
            if isinstance(item, str):
                item.rstrip()
            print '%s = %s' % ('.'.join(path), item)

    walk(list(), content)
