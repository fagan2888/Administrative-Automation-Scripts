"""
This script attempts to walk through an entire directory
and upload all files inside as separate tables to a database
Status: Error around line 29 on "Duplicate column names"
Testing Directory: Path to where many csv files are under a directory
"""
import csv
import sqlite3
import glob
import os


def do_directory(dirname, db):
    for filename in glob.glob(os.path.join(dirname, '*.csv')):
        do_file(filename, db)


def do_file(filename, db):
    with open(filename) as f:
        with db:
            data = csv.DictReader(f)
            cols = data.fieldnames
            table = os.path.splitext(os.path.basename(filename))[0]

            sql = 'drop table if exists "{}"'.format(table)
            db.execute(sql)

            colsize = 30
            sql = 'create table "{table}" ( {cols} )'.format(
                table=table,
                cols=' '.join(('%*s' % (colsize, i) for i in line.split())))
            # new: ' '.join(('%*s' % (colsize, i) for i in line.split()))
            # old: ','.join('"{}"'.format(col) for col in cols)
            db.execute(sql)

            sql = 'insert into "{table}" values ( {vals} )'.format(
                table=table,
                vals=','.join('?' for col in cols))
            db.executemany(sql, (list(map(row.get, cols)) for row in data))


if __name__ == '__main__':
    connection = sqlite3.connect('H:/rci.db')  # Path to db file
    do_directory('C:/Path/to/Directory/With/CSV_Files', connection)
