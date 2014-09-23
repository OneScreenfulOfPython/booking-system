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

def populate_database():
    """Populate the database with some valid test data
    """
    db = sqlite3.connect(DATABASE_FILEPATH)
    q = db.cursor()

    sql = "INSERT INTO users(id, name, email_address) VALUES(?, ?, ?)"
    q.execute(sql, [1, "Mickey Mouse", "mickey.mouse@example.com"])
    q.execute(sql, [2, "Donald Duck", "donald.duck@example.com"])
    q.execute(sql, [3, "Kermit the Frog", None])

    sql = "INSERT INTO rooms(id, name, location) VALUES(?, ?, ?)"
    q.execute(sql, [1, "Room A", "Next to the stairway"])
    q.execute(sql, [2, "Room B", "On the Second Floor"])
    q.execute(sql, [3, "Main Hall", None])

    #
    # Triple-quoted strings can cross lines
    # NB the column order doesn't matter if you specify it
    #
    sql = """
    INSERT INTO
        bookings
    (
        room_id, user_id, booked_on, booked_from, booked_to
    )
    VALUES(
        ?, ?, ?, ?, ?
    )"""
    q.execute(sql, [1, 1, '2014-09-25', '09:00', '10:00']) # Room A (1) booked by Mickey (1) from 9am to 10am on 25th Sep 2014
    q.execute(sql, [3, 1, '2015-09-25', None, None]) # Main Hall (3) booked by Mickey (1) from all day on 25th Sep 2014
    q.execute(sql, [2, 3, '2014-09-22', '12:00', None]) # Room B (2) booked by Kermit (3) from midday onwards on 22nd Sep 2014
    q.execute(sql, [1, 2, '2015-02-14', '09:30', '10:00']) # Room A (1) booked by Donald (2) from 9.30am to 10am on 15th Feb 2014

    q.close()
    db.commit()
    db.close()

def get_users():
    """Get all the users from the database
    """
    db = sqlite3.connect(DATABASE_FILEPATH)
    db.row_factory = sqlite3.Row
    q = db.cursor()

    q.execute("SELECT * FROM users")
    users = q.fetchall()

    q.close()
    db.close()

    return users

def get_rooms():
    """Get all the rooms from the database
    """
    db = sqlite3.connect(DATABASE_FILEPATH)
    db.row_factory = sqlite3.Row
    q = db.cursor()

    q.execute("SELECT * FROM rooms")
    rooms = q.fetchall()

    q.close()
    db.close()

    return rooms

def get_bookings_for_user(user_id):
    """Get all the bookings made by a user
    """
    db = sqlite3.connect(DATABASE_FILEPATH)
    db.row_factory = sqlite3.Row
    q = db.cursor()

    q.execute("SELECT * FROM v_bookings WHERE user_id = ?", [user_id])
    bookings = q.fetchall()

    q.close()
    db.close()

    return bookings

def get_bookings_for_room(user_id):
    """Get all the bookings made against a room
    """
    db = sqlite3.connect(DATABASE_FILEPATH)
    db.row_factory = sqlite3.Row
    q = db.cursor()

    q.execute("SELECT * FROM v_bookings WHERE user_id = ?", [user_id])
    bookings = q.fetchall()

    q.close()
    db.close()

    return bookings

if __name__ == '__main__':
    print("About to create database %s" % DATABASE_FILEPATH)
    create_database()
    print("About to populate database %s" % DATABASE_FILEPATH)
    populate_database()
    print("Bookings for user: 1")
    for booking in get_bookings_for_user(1):
        print(booking['room_name'], booking['booked_on'])
    print("Bookings for room: 2")
    for booking in get_bookings_for_room(2):
        print(booking['user_name'], booking['booked_on'])
    print("Finished")
