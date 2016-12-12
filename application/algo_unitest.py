import unittest
from Algorithm import UseThread
import sys
import psycopg2


class TestCase(unittest.TestCase):
    def setUp(self):
        self.instance = UseThread(0)

    def tearDown(self):
        self.instance = None

    def test_cal_current_time(self):
        self.assertEqual(self.instance.cal_current_time('2016-12-10 08:12:49.510760'), 29569.510760,
                         'incorrect Time calculation')

    def test_cal_interval_time(self):
        self.assertEqual(self.instance.cal_interval_time(10000, 500, 100), 4000,
                         'incorrect Time calculation')

    def set_up(self):
        connection = self.instance.connect_database()
        assert connection != 1
        print "connect to database"
        return connection

    def test_database_clean(self):
        connection = self.set_up()
        cursor = connection.cursor()
        self.instance.database_cleanup(connection, cursor)
        print "database cleaned"

    def test_database_insert(self):
        # conn = psycopg2.connect("host='localhost' dbname='stock' user='postgres' password=''")
        # cursor = conn.cursor()
        conn = self.set_up()
        cursor = conn.cursor()
        cursor.execute('SELECT count(*) FROM transact')
        row_count = 0
        for row in cursor:
            row_count += 1
            print "row: %s    %s\n" % (row_count, row)
        sell_info = {'trans_id': 1, 'total_sell': 0, 'sum_value': 0.0, 'avg': 0.0, 'plan_value': 10000}
        self.instance.insert_trans(sell_info, "failure occurred, recalculate strategy", None, cursor, conn)
        try:
            self.instance.insert_trans(sell_info, "failure occurred, recalculate strategy", None, None, conn)
        except Exception as info:
            print info
            print "Pass exception test"

if __name__ == '__main__':
    unittest.main()
