I've pulled the main create statements out into a separate .sql file, both
because they're quite bulky text to include directly in Python code, and
because it's a fairly decent technique to pull text in and execute it against
the database.

You could do the same thing (and more easily) via the command-line if you
had access to the sqlite.exe executable:

sqlite < create.sql

For simplicity, I've avoided with-statements and try-finally blocks.
For more robust code, you'd normally use one or other of these (depending
mostly on whether the code had been set up with context managers). You're
looking at something like this:

with open("create.sql") as f:
  text = f.read()

or

db = sql.connect("...")
try:
    ...
finally:
    db.close()
