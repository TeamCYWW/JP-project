import unittest
from Algorithm import UseThread
import psycopg2



class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.instance = UseThread(0)

    def tearDown(self):
        self.instance.exit()
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
        conn = psycopg2.connect("dbname='stock' user='postgres' host='localhost' password='' ")
        print conn
        cursor = conn.cursor()
        a = cursor.execute("""SELECT count(*) FROM user_info;""")
        print a
        for row in a:
            print row

        sell_info = {'trans_id': 1, 'total_sell': 0, 'sum_value': 0.0, 'avg': 0.0}
        # self.instance.insert_trans(sell_info, "failure occurred, recalculate strategy", None, connection, cursor)


if __name__ == '__main__':
    unittest.main()
