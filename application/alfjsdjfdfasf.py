import psycopg2
from Algorithm import UseThread
import threading

conn_string = "host='localhost' dbname='stock' user='postgres' password='secret'"
conn = psycopg2.connect(conn_string)

# HERE IS THE IMPORTANT PART, by specifying a name for the cursor
# psycopg2 creates a server-side cursor, which prevents all of the
# records from being downloaded at once from the server.
cursor = conn.cursor()
cursor.execute('SELECT * FROM user_info')

# Because cursor objects are iterable we can just call 'for - in' on
# the cursor object and the cursor will automatically advance itself
# each iteration.
# This loop should run 1000 times, assuming there are at least 1000
# records in 'my_table'
row_count = 0
for row in cursor:
    row_count += 1
    print "row: %s    %s\n" % (row_count, row)
app = UseThread.run()
app.exit

class UseThread(threading.Thread):
    """
    This is algorithm class which is thread class' extension
    """

    def __init__(self, quantity):
        """
        class initiator
        """
        threading.Thread.__init__(self)
        self.quantity = quantity
        self.exit_flag = False
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def exit(self):
        self.exit_flag = True
        return "Stop"

    @staticmethod
    def is_run():
        return True

