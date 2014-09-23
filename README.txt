Build a booking system (ostensibly for Rooms but could be for
anything: gym equipment, library books etc.).

Meta-Requirement:

* Only use built-in modules (but suggest alternatives)

* Run unchanged on Python 2 and 3

* Run unchanged on any Python-supported platform (esp. including RPi)

* Keep core code simple, without using any more sophisticated Python idioms,
  but suggest alternatives / improvements.

* Remain import-table to allow for experimentation. This is especially
  useful as it makes it possible to experiment easily at the command
  line, eg:

  import bookings

  bookings.create_database()
  bookings.populate_database()
  print(bookings.get_user(1))
  print(bookings.get_room(1))
  bookings.add_booking_to_database(1, 1, '2014-11-18', '12:00')


Project Requirements:

* People have names & email addresses

* Rooms have names and locations

* Bookings are made by one person for one room on one day between Time A and Time B

* There should be a usable interface to book rooms / view room bookings

Steps -- each intended to be about a screenful. Each step leaves the
application in a "working" state, albeit not necessarily a very interesting
one, at least at first.

1) Create the empty database

2) Populate with some sample data: users, rooms, bookings

3) Create simple functions for accessing users & rooms

4) Create simple functions for accessing bookings via users & rooms

5) Refactor the database queries to use common functionality

6) Create a simple website with just a front page

7) Add /users to list users & /rooms to list rooms

8) Refactor the HTML pages to use common functionality

9) Add /bookings to list bookings for a user or a room

10) Add a user

11) Add a room

12) Add a booking (of a room by a user)

13) Add a booking (by a user of a room)

14) Show all bookings and allow additions

Hints:

* You can use the sqlite ".dump" command to quickly see the database contents:

  sqlite bookings.db .dump

