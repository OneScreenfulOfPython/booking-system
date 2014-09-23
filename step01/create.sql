CREATE TABLE
    users
(
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(200) NOT NULL,
    email_address VARCHAR(200) NULL
)
;

CREATE TABLE
    rooms
(
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(200) NOT NULL,
    location VARCHAR(1024) NULL
)
;

CREATE TABLE
    bookings
(
    user_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    booked_on DATE NOT NULL,
    booked_from TIME NULL,
    booked_to TIME NULL
)
;

CREATE VIEW
    v_bookings
AS SELECT
    boo.user_id,
    usr.name AS user_name,
    boo.room_id,
    roo.name AS room_name,
    boo.booked_on,
    boo.booked_from,
    boo.booked_to
FROM
    bookings AS boo
JOIN users AS usr ON
    usr.id = boo.user_id
JOIN rooms AS roo ON
    roo.id = boo.room_id
;
