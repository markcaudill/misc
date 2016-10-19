#!/usr/bin/env python3

import sqlite3
import time


class ChangeLog(object):
    """
    A log that tracks changes of named items. Similar to a key=value store
    (where both key and value are strings) except a history of the values and
    when they change is kept.
    """
    def __init__(self, db):
        """
        Initialize the object and create the database if it does not
        already exist.

        :param db: the filename of the SQLite database
        :type  db: str
        """
        self.db = db
        self.create_db()

    def create_db(self):
        """
        Create the scheme in the database.
        """
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS checks (
            name TEXT,
            timestamp INTEGER,
            checksum TEXT)
            """)
        conn.commit()
        conn.close()

    def get_last_value(self, name):
        """
        Fetch the latest value of name.

        :param name: the name to check
        :type  name: str
        :returns: the latest value available
        :rtype: str
        """
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute(
            """
            SELECT checksum FROM checks
            WHERE name = ?
            ORDER BY timestamp
            DESC LIMIT 1""", (name,))
        value = c.fetchone()[0]
        conn.close()
        return value

    def update_value(self, name, value):
        """
        Update the value of name.

        :param name: the name to update
        :type  name: str
        :param value: the value to use
        :type  value: str
        """
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO checks (name, timestamp, checksum)
            VALUES (?, ?, ?)
            """, (name, time.time(), value))
        conn.commit()
        conn.close()


def main():
    import argparse
    import hashlib
    import os
    import sys

    parser = argparse.ArgumentParser(
        description='hash stdin and return 1 if it has changed')
    parser.add_argument(
        '--name', help='the name of the check', type=str, required=True)
    parser.add_argument(
        '--db', help='the SQLite3 DB to use for tracking state',
        default='%s/.ischanged.db' % os.path.expanduser('~'))
    parser.add_argument(
        '--verbose', help='output text as well as return values',
        action='store_true', default=False)
    args = parser.parse_args()

    m = hashlib.sha256()
    cldb = ChangeLog(args.db)

    # Hash STDIN
    for line in sys.stdin.readlines():
        m.update(line.encode())
    new_hash = m.hexdigest()
    # Compare with the last known value
    old_hash = cldb.get_last_value(args.name)
    if new_hash != old_hash:
        if args.verbose:
            print("Old Hash: ", old_hash, "\nNew Hash: ", new_hash)
        # Update the DB
        cldb.update_value(args.name, new_hash)
        sys.exit(1)
    else:
        if args.verbose:
            print('No change.')
        sys.exit(0)

if __name__ == '__main__':
    main()
