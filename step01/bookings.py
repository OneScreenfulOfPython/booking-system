#!python3
import os, sys
import sqlite3

#
# Ensure we're using the same database filename throughout.
# It doesn't matter what this is called or where it is:
# sqlite3 will just accept anything.
#
DATABASE_FILEPATH = "bookings.db"
def create_database():
    """Connect to the database, read the CREATE statements and split
    them at the semicolon into individual statements. Once each
    statement has been executed, close the connection.
    """
    #
    # Since we might be re-running this, delete the file and rebuild
    # it if necessary.
    #
    if os.path.exists(DATABASE_FILEPATH):
        os.remove(DATABASE_FILEPATH)

    #
    # A database cursor the the Python mechanism for running something
    # against any database. You create a cursor and then .execute
    # SQL statements through it.
    #
    db = sqlite3.connect(DATABASE_FILEPATH)
    q = db.cursor()

    #
    # Read all the contents of create.sql in one gulp
    #
    sql = open("create.sql").read()
    #
    # Split it into individual statements, breaking on the semicolon
    #
    statements = sql.split(";")
    #
    # Execute each of the individual statements against the database
    #
    for statement in statements:
        q.execute(statement)

    #
    # Close everything
    #
    q.close()
    db.commit()
    db.close()

if __name__ == '__main__':
    print("About to create database %s" % DATABASE_FILEPATH)
    create_database()
    print("Finished")
