I've used the simplest possible approach to retrieve the users and rooms.
In particular, I've avoided try-finally and with-statements, both of which
would typically apply here. You could rework the code like this:

def get_users():
    """Get all the users from the database
    """
    db = sqlite3.connect(DATABASE_FILEPATH)
    db.row_factory = sqlite3.Row
    q = db.cursor()
    try:
        q.execute("SELECT * FROM users")
        users = q.fetchall()
        return users
    finally:
        q.close()
        db.close()

and you could also refactor slightly, since "users" no longer needs
to be named; you could just return the result of q.fetchall().

I haven't approached the bookings data here as this is more complicated.