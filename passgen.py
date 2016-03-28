#!/usr/bin/env python

from argparse import ArgumentParser
from random import choice
from string import digits, letters, punctuation

parser = ArgumentParser(description=u'Generate a password.')
parser.add_argument('--length', type=int, help=u'The length of the password.',
        default=16)
args = parser.parse_args()

def gen_password(characters, length):
    return u''.join([choice(characters) for _ in xrange(length)])

def main():
    password = gen_password(digits + letters + punctuation, args.length)
    print(password)

if __name__ == '__main__':
    main()
