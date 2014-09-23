#!python3
import os, sys
import sqlite3
from wsgiref.util import setup_testing_defaults, shift_path_info
from wsgiref.simple_server import make_server

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

def select(sql_statement, params=None):
    """General-purpose routine to read from the database
    """
    if params is None:
        params = []
    db = sqlite3.connect(DATABASE_FILEPATH)
    db.row_factory = sqlite3.Row
    q = db.cursor()
    try:
        q.execute(sql_statement, params)
        return q.fetchall()
    finally:
        q.close()
        db.close()

def get_users():
    """Get all the users from the database
    """
    return select("SELECT * FROM users")

def get_rooms():
    """Get all the rooms from the database
    """
    return select("SELECT * FROM rooms")

def get_bookings_for_user(user_id):
    """Get all the bookings made by a user
    """
    return select("SELECT * FROM v_bookings WHERE user_id = ?", [user_id])

def get_bookings_for_room(room_id):
    """Get all the bookings made against a room
    """
    return select("SELECT * FROM v_bookings WHERE room_id = ?", [room_id])

def page(title, content):
    """Return a complete HTML page with the title as the <title> and <h1>
    tags, and the content within the body, after the <h1>
    """
    return """
    <html>
    <head>
    <title>Room Booking System: {title}</title>
    <style>
    body {{
        background-colour : #cff;
        margin : 1em;
        padding : 1em;
        border : thin solid black;
        font-family : sans-serif;
    }}
    td {{
        padding : 0.5em;
        margin : 0.5em;
        border : thin solid blue;
    }}

    </style>
    </head>
    <body>
    <h1>{title}</h1>
    {content}
    </body>
    </html>
    """.format(title=title, content=content)

def index_page(environ):
    """Provide a list of all the pages
    """
    html = """
    <ul>
        <li><a href="/users">Users</a></li>
        <li><a href="/rooms">Rooms</a></li>
        <li><a href="/bookings">Bookings</a></li>
    </ul>
    """
    return page("Starting Page", html)

def users_page(environ):
    """Provide a list of all the users, linking to their bookings
    """
    html = "<ul>"
    for user in get_users():
        html += '<li><a href="/bookings/user/{id}">{name}</a> ({email_address})</li>\n'.format(
            id=user['id'],
            name=user['name'],
            email_address=user['email_address'] or "No email"
        )
    html += "</ul>"
    return page("Users", html)

def rooms_page(environ):
    """Provide a list of all the rooms, linking to their bookings
    """
    html = "<ul>"
    for room in get_rooms():
        html += '<li><a href="/bookings/room/{id}">{name}</a> ({location})</li>\n'.format(
            id=room['id'],
            name=room['name'],
            location=room['location'] or "Location unknown"
        )
    html += "</ul>"
    return page("Rooms", html)

def bookings_user_page(environ):
    """Provide a list of bookings by user, showing room and date/time
    """
    user_id = int(shift_path_info(environ))
    html = "<table>"
    html += "<tr><td>Room</td><td>Date</td><td>Times</td></tr>"
    for booking in get_bookings_for_user(user_id):
        html += "<tr><td>{room_name}</td><td>{booked_on}</td><td>{booked_from} - {booked_to}</td></tr>".format(
            room_name=booking['room_name'],
            booked_on=booking['booked_on'],
            booked_from=booking['booked_from'] or "",
            booked_to=booking['booked_to'] or ""
        )
    html += "</table>"
    return page("Bookings for user %d" % user_id, html)

def bookings_room_page(environ):
    """Provide a list of bookings by room, showing user and date/time
    """
    room_id = int(shift_path_info(environ))
    html = "<table>"
    html += "<tr><td>User</td><td>Date</td><td>Times</td></tr>"
    for booking in get_bookings_for_room(room_id):
        html += "<tr><td>{user_name}</td><td>{booked_on}</td><td>{booked_from} - {booked_to}</td></tr>".format(
            user_name=booking['user_name'],
            booked_on=booking['booked_on'],
            booked_from=booking['booked_from'] or "",
            booked_to=booking['booked_to'] or ""
        )
    html += "</table>"
    return page("Bookings for room %d" % room_id, html)

def bookings_page(environ):
    """Provide a list of all bookings by a user or room, showing
    the other thing (room or user) and the date/time
    """
    category = shift_path_info(environ)
    if category == "user":
        return bookings_user_page(environ)
    elif category == "room":
        return bookings_room_page(environ)
    else:
        return "No such booking category"

def webapp(environ, start_response):
    """Serve simple pages, based on whether the URL requests
    users, rooms or bookings. For now, just serve the Home page
    """
    setup_testing_defaults(environ)

    #
    # Assume we're going to serve a valid HTML page
    #
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    #
    # Pick up the first segment on the path and pass
    # the rest along.
    #
    # ie if we're looking for /users/1/bookings,
    # param1 will be "users", and the remaining path will
    # be "/1/bookings".
    #
    param1 = shift_path_info(environ)
    if param1 == "":
        data = index_page(environ)
    elif param1 == "users":
        data = users_page(environ)
    elif param1 == "rooms":
        data = rooms_page(environ)
    elif param1 == "bookings":
        data = bookings_page(environ)
    else:
        status = '404 Not Found'
        data = "Not Found: %s" % param1

    start_response(status, headers)
    return [data.encode("utf-8")]

def run_website():
    httpd = make_server('', 8000, webapp)
    print("Serving on port 8000...")
    httpd.serve_forever()

if __name__ == '__main__':
    print("About to create database %s" % DATABASE_FILEPATH)
    create_database()
    print("About to populate database %s" % DATABASE_FILEPATH)
    populate_database()
    print("About to run webserver")
    run_website()
    print("Finished")
