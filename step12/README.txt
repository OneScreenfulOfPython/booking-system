Add a booking from a user's page
Add a booking from a room's page

Quite a lot happening here as this is bringing together all the pieces
of data we have. There's next to no validation on the form at front or
backend. And sqlite is extremely forgiving (it basically stores everything
as text regardless of the column's datatype). So there's real scope here
for messing around with data.

Note: the same code (add_booking) is used from both forms: each has the
same information (user_id, room_id, when) and in each case one is
selected by the user while the other is supplied -- hidden -- by the
computer.
