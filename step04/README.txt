Add functions to retrieve all bookings for a particular user or room.

I've used the database view v_bookings which does the necessary joins
to bring the users, rooms & bookings together. An alternative is to join
separately within Python.