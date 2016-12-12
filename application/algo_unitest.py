import unittest
from Algorithm import UseThread
import sys
import psycopg2


class TestCase(unittest.TestCase):
    def setUp(self):
        self.instance = UseThread(10)

    def tearDown(self):
        self.instance = None

    def test_cal_current_time(self):
        self.assertEqual(self.instance.cal_current_time('2016-12-10 08:12:49.510760'), 29569.510760,
                         'incorrect Time calculation')
        try:
            self.instance.cal_current_time('2016-12-10 08:40:49.510760')
        except SystemExit as info:
            print info

    def test_cal_interval_time(self):
        self.assertEqual(self.instance.cal_interval_time(10000, 500, 100), 4000,
                         'incorrect Time calculation')
        self.assertEqual(self.instance.cal_interval_time(39000, 500, 100), 0,
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
        self.instance.database_cleanup(connection, None)
        print "Test to fail clean database"

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
        except SystemExit as info:
            print info
            print "Pass exception test"

    def test_quote_info(self):
        rv = self.instance.quote_info()
        print rv

    def test_make_order(self, ):
        market_info = {'top_bid': {'price': 104}}
        rv = self.instance.make_order(100, market_info, 10)
        print rv
        market_info = {'top_bid': {'price': 9999999}}
        rv = self.instance.make_order("hello", market_info, -20)
        print rv

    def test_run(self):
        self.instance.run()
        self.instance = UseThread(30)
        self.instance.run()
        self.instance = UseThread(0)
        self.instance.run()
if __name__ == '__main__':
    unittest.main()
