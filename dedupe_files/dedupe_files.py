#!/usr/bin/env python

import argparse
import hashlib
import os
import shutil


def recursive_directory_list(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)

def main():
    parser = argparse.ArgumentParser(description='Move duplicate files')
    parser.add_argument('--dry-run', action='store_true', default=False)
    parser.add_argument('--src', required=True,
            help='the directory to look for duplicates in')
    parser.add_argument('--dest', required=True,
            help='the directory to move duplicates to')
    args = parser.parse_args()

    if not args.dry_run:
        try:
            os.mkdir(args.dest)
        except OSError:
            pass
    else:
        print 'Skipping mkdir %s' % args.dest

    hashes = {}
    for file in recursive_directory_list(args.src):
        file_hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
        if file_hash in hashes.keys():
            print '%s is a duplicate of %s (%s)' % (
                    file, hashes[file_hash], file_hash)
            if not args.dry_run:
                print 'Moving %s to %s' % (file, args.dest)
                shutil.move(file, args.dest)
        else:
            hashes[file_hash] = file

if __name__ == '__main__':
    main()
