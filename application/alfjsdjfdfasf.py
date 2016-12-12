import psycopg2
from Algorithm import UseThread
import threading

conn_string = "host='localhost' dbname='stock' user='postgres' password=''"
conn = psycopg2.connect("host='localhost' dbname='stock' user='postgres' password=''")

# HERE IS THE IMPORTANT PART, by specifying a name for the cursor
# psycopg2 creates a server-side cursor, which prevents all of the
# records from being downloaded at once from the server.
cursor = conn.cursor()
cursor.execute('SELECT * FROM user_info')

row_count = 0
for row in cursor:
    row_count += 1
    print "row: %s    %s\n" % (row_count, row)

