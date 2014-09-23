For simplicity, I've hardwired names etc. into the inline INSERT statements.
A more sophisticated approach could use CSV files to hold the initial data.
Assuming that you had a CSV file of rooms called rooms.csv:

Room A, Next to the stairway
Room B, On the Second Floor
Main Hall,

you could do something like this:

import csv
import sqlite3


db = sqlite.connect("...")
q = db.cursor()

f = open("rooms.csv", "b")
reader = csv.reader(f)
for row in reader:
  q.execute("INSERT INTO rooms(name, location) VALUES (?, ?)", row)

q.close()
db.commit()
db.close()


I've sidestepped the fact that sqlite will auto-generate primary key ids
if a column is specified as INTEGER PRIMARY KEY. This is to make the test
data inserts easier to read. The csv code above *does* assume that sqlite
will autogenerate ids.